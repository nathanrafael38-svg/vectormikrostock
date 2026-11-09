"""PNG hasil AI -> vector bersih + teks font OFL -> master SVG (pt) -> EPS + JPG -> QC.
Pemakaian: python -m agent_vector <job.json>"""
import io, json, math, os, re, subprocess, sys, shutil
import numpy as np
from PIL import Image, ImageFilter
import vtracer
from . import textpath

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(HERE, 'fonts')
W_PT, H_PT = 5334, 3000

def log(*a): print('[badge]', *a, flush=True)

# ---------- 1. raster prep ----------
def nearest(arr, pal):
    flat = arr.reshape(-1, 3)
    out = np.empty(len(flat), np.int32)
    for i in range(0, len(flat), 500000):
        ch = flat[i:i+500000]
        out[i:i+500000] = ((ch[:, None, :] - pal[None, :, :]) ** 2).sum(-1).argmin(1)
    return out.reshape(arr.shape[:2])

def kmeans_palette(arr, k, iters=25, merge=28):
    rng = np.random.default_rng(0)
    px = arr.reshape(-1, 3)[rng.choice(arr.shape[0]*arr.shape[1], 60000, replace=False)]
    cent = [px[rng.integers(len(px))]]
    for _ in range(k - 1):  # k-means++
        d = np.min(((px[:, None] - np.array(cent)[None]) ** 2).sum(-1), 1)
        cent.append(px[rng.choice(len(px), p=d / d.sum())])
    cent = np.array(cent)
    for _ in range(iters):
        lab = ((px[:, None] - cent[None]) ** 2).sum(-1).argmin(1)
        cent = np.array([px[lab == j].mean(0) if (lab == j).any() else cent[j] for j in range(k)])
    keep = []  # gabung warna yang hampir sama (pinggiran antialias)
    for c in cent:
        if all(np.sqrt(((c - q) ** 2).sum()) > merge for q in keep): keep.append(c)
    return np.array(keep)

def prep(png, n_colors, upscale, bg_tol, masks=()):
    im = Image.open(png).convert('RGB')
    w0, h0 = im.size
    if upscale > 1:
        im = im.resize((w0 * upscale, h0 * upscale), Image.LANCZOS)
    paint_masks(im, masks, w0 * upscale, h0 * upscale)
    im = im.filter(ImageFilter.MedianFilter(5))
    arr = np.asarray(im).astype(np.float32)
    pal = kmeans_palette(arr, n_colors)
    idx = nearest(arr, pal)
    q2 = Image.fromarray(idx.astype(np.uint8)).filter(ImageFilter.ModeFilter(7))
    idx = np.array(q2)
    pal = pal.astype(int)
    rgb = pal[idx].astype(np.uint8)
    # buang background luar: flood fill dari tepi untuk warna yang dekat warna pojok
    corner = rgb[0, 0].astype(int)
    near = (np.abs(rgb.astype(int) - corner).sum(axis=2) <= bg_tol)
    mask = np.zeros(near.shape, bool)
    from collections import deque
    h, w = near.shape
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not mask[y, x]: mask[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not mask[y, x]: mask[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for yy, xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if 0 <= yy < h and 0 <= xx < w and near[yy, xx] and not mask[yy, xx]:
                mask[yy, xx] = True; dq.append((yy, xx))
    rgba = np.dstack([rgb, np.where(mask, 0, 255).astype(np.uint8)])
    return Image.fromarray(rgba, 'RGBA'), (w0, h0), [tuple(int(v) for v in p) for p in pal]

# ---------- 2. trace ----------
def trace(img, speckle, upscale):
    buf = io.BytesIO(); img.save(buf, 'PNG')
    svg = vtracer.convert_raw_image_to_svg(buf.getvalue(), img_format='png', colormode='color',
        hierarchical='stacked', mode='spline', filter_speckle=speckle * upscale, color_precision=8,
        layer_difference=8, corner_threshold=60, length_threshold=4.0, max_iterations=10,
        splice_threshold=45, path_precision=3)
    paths = []
    for m in re.finditer(r'<path d="([^"]+)" fill="([^"]+)" transform="translate\(([-\d.]+),([-\d.]+)\)"', svg):
        d, fill, tx, ty = m.group(1), m.group(2), float(m.group(3)), float(m.group(4))
        paths.append((d, fill.upper(), tx, ty))
    return paths

def snap_fill(fill, palette):
    """vtracer kadang kasih warna rata-rata; snap ke palet terdekat."""
    r, g, b = int(fill[1:3], 16), int(fill[3:5], 16), int(fill[5:7], 16)
    best = min(palette, key=lambda p: (p[0]-r)**2 + (p[1]-g)**2 + (p[2]-b)**2)
    return '#%02X%02X%02X' % best

def node_count(d):
    return len(re.findall(r'[MLCQZmlcqz]', d))

# ---------- 3. compose ----------
def paint_masks(im, masks, W, H):
    """Tutup teks sampah buatan AI di raster SEBELUM tracing, supaya tidak ada path tersembunyi."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    for m in masks:
        f = m['fill']
        if m['shape'] == 'rect':
            d.rectangle([m['x']*W, m['y']*H, (m['x']+m['w'])*W, (m['y']+m['h'])*H], fill=f)
        elif m['shape'] == 'ring':
            cx, cy = m['cx']*W, m['cy']*H
            ro, ri = m['r_out']*H, m['r_in']*H
            d.ellipse([cx-ro, cy-ro, cx+ro, cy+ro], outline=f, width=int(ro-ri))
        elif m['shape'] == 'polygon':
            d.polygon([(x*W, y*H) for x, y in m['points']], fill=f)

def font(name):
    p = os.path.join(FONTS, name)
    if not os.path.exists(p): raise SystemExit(f'font tidak ada: {p}')
    return p

def text_elems(texts, w0, h0):
    """Koordinat teks dalam pecahan ukuran gambar (0..1) -> path di ruang piksel gambar asli."""
    out = []
    for t in texts:
        f = font(t['font']); size = t['size'] * h0; tr = t.get('tracking', 0.0)
        if t['kind'] == 'line':
            d = textpath.line(t['text'], f, size, t['cx'] * w0, t['baseline'] * h0, tr)
        else:
            d = textpath.arc(t['text'], f, size, t['cx'] * w0, t['cy'] * h0, t['r'] * h0,
                             center_deg=t.get('center_deg', -90 if t['kind'] == 'arc_top' else 90),
                             tracking=tr, bottom=(t['kind'] == 'arc_bottom'))
        out.append((d, t['color'].upper()))
    return out

def mask_rects(masks, w0, h0, fill):
    """Kotak/lingkaran penutup untuk menghapus teks sampah buatan AI sebelum teks asli ditaruh."""
    out = []
    for m in masks:
        if m['shape'] == 'rect':
            x, y, w, h = m['x']*w0, m['y']*h0, m['w']*w0, m['h']*h0
            out.append((f'M{x:.2f} {y:.2f}H{x+w:.2f}V{y+h:.2f}H{x:.2f}Z', m.get('fill', fill).upper()))
        elif m['shape'] == 'ring':   # cincin (untuk pita teks melingkar)
            cx, cy, r1, r2 = m['cx']*w0, m['cy']*h0, m['r_in']*h0, m['r_out']*h0
            def circ(r): return f'M{cx-r:.2f} {cy:.2f}A{r:.2f} {r:.2f} 0 1 0 {cx+r:.2f} {cy:.2f}A{r:.2f} {r:.2f} 0 1 0 {cx-r:.2f} {cy:.2f}Z'
            out.append((circ(r2) + circ(r1), m.get('fill', fill).upper()))
    return out

def group_svg(paths, texts, masks, recolor=None, upscale=1):
    parts = [f'<g transform="scale({1/upscale:.6f})">']
    for d, fill, tx, ty in paths:
        f = recolor(fill) if recolor else fill
        parts.append(f'<path d="{d}" fill="{f}" transform="translate({tx:.2f},{ty:.2f})"/>')
    parts.append('</g>')
    for d, fill in masks:
        f = recolor(fill) if recolor else fill
        parts.append(f'<path d="{d}" fill="{f}" fill-rule="evenodd"/>')
    for d, fill in texts:
        f = recolor(fill) if recolor else fill
        parts.append(f'<path d="{d}" fill="{f}"/>')
    return '\n'.join(parts)

def compose(job, paths, texts, masks, w0, h0):
    bg = job.get('artboard_bg', '#FFFFFF')  # wajib: tanpa latar, cairo memotong BoundingBox
    layout = 'primary_plus_variant' if job.get('variant_map') else 'single'
    blocks = []
    if layout == 'single':
        slots = [(W_PT/2, None)]
    else:
        slots = [(W_PT*0.30, None), (W_PT*0.74, 'mono')]
    hgt = H_PT * job.get('logo_height', 0.78)
    for cx, mode in slots:
        s = hgt / h0
        x = cx - w0*s/2; y = (H_PT - h0*s)/2
        rec = None
        if mode == 'mono':
            mono = job.get('mono_color', '#1A1A1A').upper()
            vmap = {k.upper(): v.upper() for k, v in job['variant_map'].items()}
            keys = list(vmap)
            def rgb(h): return int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
            def rec(f, vmap=vmap, keys=keys):
                r, g, b = rgb(f)
                k = min(keys, key=lambda c: sum((a-q)**2 for a, q in zip(rgb(c), (r, g, b))))
                return vmap[k]
            hgt2 = hgt * 0.72; s = hgt2 / h0; x = cx - w0*s/2; y = (H_PT - h0*s)/2
        blocks.append(f'<g id="{mode or "primary"}" transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">\n'
                      + group_svg(paths, texts, masks, rec, job.get('upscale', 2)) + '\n</g>')
    bgrect = f'<rect x="0" y="0" width="{W_PT}" height="{H_PT}" fill="{bg}"/>' if bg else ''
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{W_PT}pt" height="{H_PT}pt" viewBox="0 0 {W_PT} {H_PT}">\n{bgrect}\n' + '\n'.join(blocks) + '\n</svg>\n')

# ---------- 4. export + QC ----------
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f'gagal: {" ".join(cmd)}\n{r.stderr[-800:]}')

def export(svg_path, eps_path, jpg_path):
    run(['inkscape', svg_path, '--export-type=eps', '--export-area-page', '--export-ps-level=3',
         '--export-text-to-path', f'--export-filename={eps_path}'])
    png = jpg_path[:-4] + '_tmp.png'
    run(['inkscape', svg_path, '--export-type=png', '--export-area-page', '--export-width=2667',
         '--export-background=#FFFFFF', '--export-background-opacity=1', f'--export-filename={png}'])
    Image.open(png).convert('RGB').save(jpg_path, quality=92); os.remove(png)

def qc(eps_path, svg_text, paths, w_jpg):
    rep = {}
    raw = open(eps_path, 'rb').read().decode('latin-1')
    body = raw.split('%%EndProlog', 1)[-1]
    rep['raster_tertanam'] = bool(re.search(r'/DataSource|/ImageType|\bcolorimage\b', body))
    m = re.search(r'%%BoundingBox:\s*(\d+) (\d+) (\d+) (\d+)', raw)
    rep['boundingbox'] = m.group(0) if m else None
    bw, bh = (int(m.group(3)) - int(m.group(1)), int(m.group(4)) - int(m.group(2))) if m else (0, 0)
    rep['megapixel'] = round(bw * bh / 1e6, 2)
    rep['ukuran_kb'] = round(os.path.getsize(eps_path) / 1024, 1)
    rep['jumlah_path_logo'] = len(paths)
    rep['total_node_logo'] = sum(node_count(d) for d, *_ in paths)
    rep['warna'] = sorted({f for _, f, *_ in paths})
    rep['ada_tag_image_di_svg'] = '<image' in svg_text
    rep['lolos'] = (not rep['raster_tertanam'] and not rep['ada_tag_image_di_svg'] and 15 <= rep['megapixel'] <= 65
                    and rep['ukuran_kb'] < 45 * 1024)
    return rep

def main(job_path):
    job = json.load(open(job_path))
    base = os.path.dirname(os.path.abspath(job_path))
    out = os.path.join(base, job.get('out_dir', 'out')); os.makedirs(out, exist_ok=True)
    name = job['id']
    img, (w0, h0), pal = prep(os.path.join(base, job['input']), job.get('colors', 6), job.get('upscale', 2), job.get('bg_tol', 60), job.get('masks', []))
    log('palet hasil kuantisasi:', ['#%02X%02X%02X' % p for p in pal])
    img.save(os.path.join(out, f'{name}_step1_flat.png'))
    paths = trace(img, job.get('speckle', 6), job.get('upscale', 2))
    paths = [(d, snap_fill(f, pal), tx, ty) for d, f, tx, ty in paths]
    drop = {c.upper() for c in job.get('drop_colors', [])}
    paths = [p for p in paths if p[1] not in drop]
    remap = {k.upper(): v.upper() for k, v in job.get('recolor', {}).items()}
    paths = [(d, remap.get(f, f), tx, ty) for d, f, tx, ty in paths]
    texts = text_elems(job.get('texts', []), w0, h0)
    masks = []  # sudah dicat di raster
    svg = compose(job, paths, texts, masks, w0, h0)
    svg_path = os.path.join(out, f'{name}_master.svg'); open(svg_path, 'w').write(svg)
    eps_path = os.path.join(out, f'{name}.eps'); jpg_path = os.path.join(out, f'{name}_preview.jpg')
    export(svg_path, eps_path, jpg_path)
    rep = qc(eps_path, svg, paths, 2667)
    json.dump(rep, open(os.path.join(out, f'{name}_qc.json'), 'w'), indent=2)
    for k, v in rep.items(): log(f'{k}: {v}')
    return rep

if __name__ == '__main__':
    main(sys.argv[1])
