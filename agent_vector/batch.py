"""Mode batch: satu folder PNG hasil Flow -> EPS + preview + QC + contact sheet + CSV metadata draft.
python -m agent_vector.batch <folder_inbox> [--registry data/registry.json]
Nama file harus diawali ID: logo-012.png, logo-012_v2.png, dst.
Override per gambar: taruh <id>.json di folder yang sama (isi sama seperti job.json, tanpa id/input)."""
import argparse, csv, glob, json, os, re, shutil, sys
from PIL import Image, ImageDraw
from . import pipeline

DEFAULTS = dict(colors=6, upscale=2, speckle=8, bg_tol=60, logo_height=0.78)
BASE_KW = ['logo', 'badge', 'emblem', 'vintage', 'retro', 'symbol', 'identity', 'branding', 'template', 'vector',
           'flat', 'illustration', 'business', 'service', 'company', 'design', 'icon', 'isolated', 'white background']

def dhash(path, n=16):
    im = Image.open(path).convert('L').resize((n + 1, n))
    px = list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())
    return sum(1 << i for i, (a, b) in enumerate((px[r*(n+1)+c], px[r*(n+1)+c+1]) for r in range(n) for c in range(n)) if a > b)

def hamming(a, b): return bin(a ^ b).count('1')

def niche_map(reg_path):
    if not reg_path or not os.path.exists(reg_path): return {}
    return {u['id']: u['niche'] for u in json.load(open(reg_path))['used']}

def draft_meta(i, niche):
    n = niche or 'Business'
    title = f'Vintage Badge Logo Emblem for {n} Business'
    kws = [w.strip().lower() for w in re.split(r'[/,&]', n) if w.strip()] + BASE_KW
    seen, out = set(), []
    for k in kws:
        if k not in seen: seen.add(k); out.append(k)
    return title[:200], out[:49]

def run(inbox, reg_path=None, outroot=None):
    pngs = sorted(p for p in glob.glob(os.path.join(inbox, '*')) if p.lower().endswith(('.png', '.jpg', '.jpeg')))
    if not pngs: raise SystemExit('folder kosong: tidak ada gambar')
    outroot = outroot or os.path.join(inbox, 'hasil'); os.makedirs(outroot, exist_ok=True)
    niches = niche_map(reg_path); rows, reps, hashes = [], {}, {}
    for p in pngs:
        m = re.match(r'(logo-\d+)', os.path.basename(p))
        if not m: print('[batch] lewati (nama tidak diawali logo-XXX):', os.path.basename(p)); continue
        i = m.group(1)
        if i in reps: print('[batch] lewati duplikat ID', i, os.path.basename(p)); continue
        job = dict(DEFAULTS)
        ov = os.path.join(inbox, f'{i}.json')
        if os.path.exists(ov): job.update(json.load(open(ov)))
        d = os.path.join(outroot, i); os.makedirs(d, exist_ok=True)
        shutil.copy(p, os.path.join(d, 'input' + os.path.splitext(p)[1]))
        job.update(id=i, input='input' + os.path.splitext(p)[1], out_dir='.')
        jp = os.path.join(d, 'job.json'); json.dump(job, open(jp, 'w'), indent=1)
        try:
            rep = pipeline.main(jp)
        except SystemExit as e:
            rep = {'lolos': False, 'error': str(e)[:300]}
        h = dhash(p)
        near = [o for o, oh in hashes.items() if hamming(h, oh) <= 40]  # 256 bit; <=40 beda sangat kecil
        rep['mirip_dengan'] = near; hashes[i] = h; reps[i] = rep
        # catatan: warna bukan-palet & node berlebih ditandai untuk ditinjau manual
        rep['perlu_tinjau'] = bool(rep.get('total_node_logo', 0) > 6000 or near or len(rep.get('warna', [])) > 6)
        t, k = draft_meta(i, niches.get(i))
        rows.append([f'{i}.eps', t, ', '.join(k), '', ''])
        shutil.copy(os.path.join(d, f'{i}.eps'), os.path.join(outroot, f'{i}.eps')) if rep.get('lolos') else None
    with open(os.path.join(outroot, 'metadata_DRAFT_adobe.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['Filename', 'Title', 'Keywords', 'Category', 'Releases']); w.writerows(rows)
    # contact sheet preview
    prevs = [(i, os.path.join(outroot, i, f'{i}_preview.jpg')) for i in reps if os.path.exists(os.path.join(outroot, i, f'{i}_preview.jpg'))]
    if prevs:
        W, H, cols = 640, 360, 3; rws = (len(prevs) + cols - 1) // cols
        sh = Image.new('RGB', (W * cols, H * rws), 'white'); dr = ImageDraw.Draw(sh)
        for n, (i, pp) in enumerate(prevs):
            sh.paste(Image.open(pp).resize((W, H)), ((n % cols) * W, (n // cols) * H))
            dr.rectangle([(n % cols) * W, (n // cols) * H, (n % cols) * W + 90, (n // cols) * H + 16], fill='black')
            dr.text(((n % cols) * W + 3, (n // cols) * H + 3), i + ('  PERLU TINJAU' if reps[i]['perlu_tinjau'] else ''), fill='yellow')
        sh.save(os.path.join(outroot, 'contact_sheet.jpg'), quality=88)
    L = ['# Laporan batch', '', '| ID | Lolos QC teknis | MP | KB | Node | Warna | Catatan |', '|---|---|---|---|---|---|---|']
    for i, r in reps.items():
        note = r.get('error') or ('; '.join(filter(None, ['mirip ' + ','.join(r['mirip_dengan']) if r['mirip_dengan'] else '', 'tinjau manual' if r['perlu_tinjau'] else ''])))
        L.append(f"| {i} | {'ya' if r.get('lolos') else 'TIDAK'} | {r.get('megapixel','-')} | {r.get('ukuran_kb','-')} | {r.get('total_node_logo','-')} | {len(r.get('warna', []))} | {note} |")
    L += ['', 'QC teknis lolos tidak berarti lolos review Adobe. Title/keyword di CSV masih DRAFT dan harus dicek terhadap gambar sebelum upload.']
    open(os.path.join(outroot, 'LAPORAN.md'), 'w').write('\n'.join(L))
    print('\n'.join(L)); return reps

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('inbox'); ap.add_argument('--registry'); ap.add_argument('--out')
    a = ap.parse_args(); run(a.inbox, a.registry, a.out)
