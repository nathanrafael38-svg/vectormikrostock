"""Teks -> path SVG (font OFL), lurus atau melengkung di busur lingkaran."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

_cache = {}
def _font(path):
    if path not in _cache:
        f = TTFont(path)
        _cache[path] = (f, f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm)
    return _cache[path]

def _glyphs(text, font):
    f, gs, cmap, upem = _font(font)
    out = []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None: g = cmap.get(ord('?'))
        out.append((g, gs[g].width))
    return out, gs, upem

def _letter_spacing(adv, upem, tracking):
    return adv + tracking * upem

def text_width(text, font, size, tracking=0.0):
    gl, gs, upem = _glyphs(text, font)
    return sum(_letter_spacing(a, upem, tracking) for _, a in gl) * size / upem

def line(text, font, size, cx, baseline_y, tracking=0.0):
    """Teks lurus, rata tengah di cx. Koordinat SVG (y ke bawah)."""
    gl, gs, upem = _glyphs(text, font)
    s = size / upem
    x = cx - text_width(text, font, size, tracking) / 2
    pen = SVGPathPen(gs)
    for g, adv in gl:
        t = TransformPen(pen, (s, 0, 0, -s, x, baseline_y))
        gs[g].draw(t)
        x += _letter_spacing(adv, upem, tracking) * s
    return pen.getCommands()

def arc(text, font, size, cx, cy, r, center_deg=-90, tracking=0.0, bottom=False):
    """Teks di busur. center_deg: -90 = atas, 90 = bawah (derajat, y ke bawah).
    Atas: baseline di radius r, huruf menghadap keluar. Bawah: huruf menghadap ke dalam, terbaca kiri->kanan,
    baseline di radius r (cap height masuk ke dalam lingkaran)."""
    gl, gs, upem = _glyphs(text, font)
    s = size / upem
    advs = [_letter_spacing(a, upem, tracking) * s for _, a in gl]
    total = sum(advs)
    span = total / r  # radian
    pen = SVGPathPen(gs)
    if not bottom:
        a = math.radians(center_deg) - span / 2
        direction = 1
    else:
        a = math.radians(center_deg) + span / 2
        direction = -1
    for (g, _), adv in zip(gl, advs):
        mid = a + direction * (adv / 2) / r
        px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
        if not bottom:
            rot = mid + math.pi / 2          # tangen searah jarum jam, atas glyph keluar
        else:
            rot = mid - math.pi / 2          # tangen berlawanan, atas glyph ke dalam
        c, sn = math.cos(rot), math.sin(rot)
        # glyph lokal: x dari -adv/2, y font ke atas -> flip
        # matrix = R(rot) * [s,0,0,-s] lalu translate supaya titik (adv/2, 0) jatuh di (px,py)
        ox, oy = -adv / 2, 0.0
        tx = px + c * ox - sn * oy
        ty = py + sn * ox + c * oy
        m = (c * s, sn * s, sn * s, -c * s, tx, ty)
        gs[g].draw(TransformPen(pen, m))
        a += direction * adv / r
    return pen.getCommands()
