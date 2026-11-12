"""Side-view knight rig: pose(anim, i) -> parts -> shaded pixel buckets per layer. Facing RIGHT, light top-left."""
import math, zlib, struct
W = H = 128
LIGHT = (-0.55, -0.65, 0.55)
_n = math.sqrt(sum(c * c for c in LIGHT)); LIGHT = tuple(c / _n for c in LIGHT)
RAMPS = {
    "steel": ["#1f2438", "#333c5c", "#51638a", "#7f95b8", "#bccfe2", "#f1f6fb"],
    "gold":  ["#4a2c1c", "#7d4f22", "#b98332", "#e5bd5c", "#fbe9a0"],
    "red":   ["#2e1022", "#59182f", "#8f2a3c", "#c24b50", "#e8787a"],
    "brown": ["#241818", "#3f2a28", "#664538", "#8b6650"],
    "blue":  ["#141a38", "#232f63", "#364a95", "#5d7bd0"],
}
OUTLINE, SHADOW, SLIT, GLOW, RIM, FULLER = "#0f1220", "#161a2c", "#07080f", "#8fe0ff", "#6f8fd0", "#3a456b"
SMEAR1, SMEAR2 = "#dfeaf6", "#8fb4e0"
LAYERS = ["shadow", "cape", "far", "legs", "body", "fx", "head", "near"]

# ---------- shapes: (mask, bbox) ----------
def ellipse(cx, cy, rx, ry):
    return (lambda x, y: ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1, (cx - rx, cy - ry, cx + rx, cy + ry))
def poly(pts):
    def f(x, y):
        px, py, inside = x + .5, y + .5, False
        for i in range(len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: inside = not inside
        return inside
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return f, (min(xs), min(ys), max(xs), max(ys))
def capsule(p1, p2, r1, r2):
    (x1, y1), (x2, y2) = p1, p2; dx, dy = x2 - x1, y2 - y1; L2 = dx * dx + dy * dy
    def f(x, y):
        px, py = x + .5, y + .5
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L2)) if L2 else 0
        return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy)) <= r1 + (r2 - r1) * t
    r = max(r1, r2); return f, (min(x1, x2) - r, min(y1, y2) - r, max(x1, x2) + r, max(y1, y2) + r)
def rect(x0, y0, w, h): return (lambda x, y: x0 <= x < x0 + w and y0 <= y < y0 + h, (x0, y0, x0 + w, y0 + h))

class Part:
    def __init__(s, name, layer, shape, ramp, R=3, group=None, line=True, folds=False, rim=False, flat=None, clip=None):
        s.name, s.layer, s.mask, s.bbox = name, layer, shape[0], shape[1]
        s.ramp = RAMPS[ramp] if isinstance(ramp, str) else ramp; s.rampname = ramp if isinstance(ramp, str) else "x"
        s.R, s.group, s.line, s.folds, s.rim, s.flat, s.clip = R, group or name, line, folds, rim, flat, clip

def ik(p0, target, L1, L2, bend):
    dx, dy = target[0] - p0[0], target[1] - p0[1]; d = math.hypot(dx, dy) or 1e-6
    d = max(abs(L1 - L2) + 0.01, min(d, L1 + L2 - 0.01))
    ux, uy = dx / math.hypot(dx, dy or 1e-6) if (dx or dy) else 1, dy / math.hypot(dx or 1e-6, dy) if (dx or dy) else 0
    n = math.hypot(dx, dy) or 1e-6; ux, uy = dx / n, dy / n
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d); h = math.sqrt(max(L1 * L1 - a * a, 0))
    bx, by = p0[0] + ux * a, p0[1] + uy * a
    knee = (bx - uy * h * bend, by + ux * h * bend)
    return knee, (p0[0] + ux * d, p0[1] + uy * d)

# ---------- poses ----------
def smooth(t): return t * t * (3 - 2 * t)
def foot(p, S=11, Hh=7, gy=109, cx=60):
    p %= 1.0
    if p < 0.5: return (cx + S * (1 - 4 * p), gy)
    s = smooth((p - 0.5) * 2); return (cx - S + 2 * S * s, gy - Hh * math.sin(math.pi * s))

BASE = dict(hip=(60, 77), sh=(62, 45), nearFoot=(64, 109), farFoot=(55, 109), nearHand=(80, 72), farHand=(79, 56),
            ang=-22, lean=0, headdy=0, cape=0.0, sway=1.0, smear=None, tas=0)

def pose(anim, i):
    p = dict(BASE)
    if anim == "idle":
        t = i / 6; b = math.sin(2 * math.pi * t)
        p.update(sh=(62, 45 + 0.9 * b), headdy=0.5 * b, nearHand=(80, 72 + 0.8 * b), farHand=(79, 56 + 0.7 * b),
                 ang=-22 + 2.5 * math.sin(2 * math.pi * t + 0.8), cape=2 * math.pi * t, sway=1.2, hip=(60, 77 - 0.3 * b))
    elif anim == "walk":
        t = i / 8; c = math.cos(4 * math.pi * t); s = math.sin(2 * math.pi * t)
        hip = (60, 76 + 1.8 * c)
        p.update(hip=hip, sh=(62 + 0.6 * s, 45 + 1.6 * c), headdy=0.4 * c, nearFoot=foot(t), farFoot=foot(t + 0.5),
                 nearHand=(80 + 2.5 * s, 72 + 0.8 * math.sin(4 * math.pi * t)), farHand=(79 - 2 * s, 56 + 0.8 * math.sin(4 * math.pi * t + 1)),
                 ang=-22 + 3 * s, cape=2 * math.pi * t, sway=2.2, tas=3 * s)
    elif anim == "attack":
        K = [  # hand, angle, lean, nearFoot, farFoot, farHand, headdy
            dict(nearHand=(80, 72), ang=-22, lean=0, nearFoot=(64, 109), farFoot=(55, 109), farHand=(79, 56)),
            dict(nearHand=(58, 52), ang=-118, lean=-3, nearFoot=(62, 109), farFoot=(51, 109), farHand=(80, 57)),
            dict(nearHand=(52, 44), ang=-148, lean=-4.5, nearFoot=(62, 109), farFoot=(50, 109), farHand=(81, 58)),
            dict(nearHand=(84, 60), ang=-8, lean=4, nearFoot=(74, 109), farFoot=(48, 109), farHand=(77, 55), smear=(-112, -4)),
            dict(nearHand=(90, 68), ang=22, lean=5, nearFoot=(75, 109), farFoot=(49, 109), farHand=(76, 55)),
            dict(nearHand=(82, 74), ang=-12, lean=2, nearFoot=(68, 109), farFoot=(53, 109), farHand=(78, 56)),
        ][i]
        p.update(K); p["sh"] = (62 + K["lean"], 45 + (1 if i in (3, 4) else 0)); p["hip"] = (60 + K["lean"] * 0.3, 77); p["cape"] = i * 1.1; p["sway"] = 2.0 + (2 if i >= 3 else 0)
    return p

def build(p):
    """Return list of Parts (z order handled by LAYERS then insertion)."""
    P = []; add = lambda *a, **k: P.append(Part(*a, **k))
    sx, sy = p["sh"]; hx, hy = p["hip"]; lean = p["lean"]
    # shadow
    add("shadow", "shadow", ellipse(60 + lean * 0.5, 117.5, 30, 3.5), [SHADOW], R=1, line=False, flat=SHADOW)
    # cape: hangs from the back of the shoulders, always behind the torso
    rows = []
    for k in range(0, 8):
        y = sy - 2 + k * 8; f = k / 7
        cx = sx - 7 - f * 8 - p["sway"] * 3.2 * f * math.sin(p["cape"] - k * 0.7) - lean * 0.4 * (1 - f)
        w = 5 + f * 7
        rows.append((cx - w, y, cx + w, y))
    left = [(r[0], r[1]) for r in rows]; right = [(r[2], r[3]) for r in rows[::-1]]
    add("cape", "cape", poly(left + [(left[-1][0] + 4, left[-1][1] + 6), (right[0][0] - 4, right[0][1] + 6)] + right), "red", R=5, folds=True)
    # far side: leg, boot, arm, shield
    for nm, ft, lay, hipo in (("legF", p["farFoot"], "far", (hx - 1.5, hy)), ("legN", p["nearFoot"], "legs", (hx + 1.5, hy))):
        knee, ank = ik(hipo, (ft[0], ft[1]), 17.5, 17.5, -1)
        add(nm, lay, capsule(hipo, knee, 7, 5.8), "steel", R=5, group=nm + "t", rim=True)
        add(nm + "s", lay, capsule(knee, ank, 5.8, 4.6), "steel", R=4, group=nm + "s", rim=True)
        add(nm + "k", lay, ellipse(knee[0] + 2, knee[1], 4.2, 4.6), "gold", R=3.5, group=nm + "k")
        add(nm + "b", lay, capsule((ank[0] - 3, ank[1] + 2), (ank[0] + 9, ank[1] + 4), 4.6, 4.2), "brown", R=4, group=nm + "b")
    fs = (sx + 3, sy + 3); el, hand = ik(fs, p["farHand"], 14, 14, 1)
    add("farUp", "far", capsule(fs, el, 4.8, 4.2), "steel", R=4, group="farU"); add("farLo", "far", capsule(el, hand, 4.2, 3.8), "steel", R=3.5, group="farL")
    cx_, cy_ = hand[0] + 4, hand[1] - 3
    sh = [(cx_ - 7, cy_ - 12), (cx_ + 7, cy_ - 11), (cx_ + 8, cy_ + 5), (cx_ + 1, cy_ + 15), (cx_ - 7, cy_ + 6)]
    add("shield", "far", poly(sh), "gold", R=3)
    inner = [(cx_ + (x - cx_) * 0.68, cy_ + 1 + (y - cy_) * 0.68) for x, y in sh]
    add("enamel", "far", poly(inner), "blue", R=3, group="shield", line=False)
    add("cross", "far", rect(round(cx_ - 1), round(cy_ - 6), 2, 14), "gold", R=1.5, group="shield", line=False)
    add("crossH", "far", rect(round(cx_ - 4), round(cy_ - 1), 8, 2), "gold", R=1.5, group="shield", line=False)
    add("handF", "far", ellipse(hand[0], hand[1], 3.6, 3.6), "steel", R=3.5)
    # body
    add("abdomen", "body", ellipse(hx - 0.5 + lean * 0.4, 66, 9.5, 9.5), "steel", R=7, group="torso", rim=True)
    add("chest", "body", ellipse(sx - 0.5, sy + 9, 11.5, 15), "steel", R=9, group="torso", rim=True)
    add("belt", "body", rect(round(hx - 11 + lean * 0.4), 70, 22, 4), "gold", R=2)
    sw = p["tas"]
    add("tasset", "body", poly([(hx - 10, 73), (hx + 11, 73), (hx + 13 + sw * 0.3, 88), (hx + 3 + sw, 93), (hx - 6 + sw * .6, 91), (hx - 12, 86)]), "steel", R=3, rim=True)
    add("surcoat", "body", poly([(hx + 4, 73), (hx + 12, 73), (hx + 14 + sw * .3, 90), (hx + 6 + sw, 95), (hx + 2, 85)]), "red", R=2.5, folds=True)
    # head
    hdx, hdy = sx + 3 + lean * 0.3, sy - 20 + p["headdy"]
    sw2 = p["sway"]; ph = p["cape"]
    add("gorget", "head", ellipse(hdx - 1, hdy + 14, 8, 4.2), "steel", R=3.5, rim=True)
    add("plume", "head", poly([(hdx - 3, hdy - 14), (hdx + 6, hdy - 13), (hdx - 3, hdy - 6), (hdx - 14 - sw2 * 2 * math.sin(ph), hdy - 2 + sw2 * math.cos(ph)), (hdx - 11, hdy - 10 + sw2 * 0.5 * math.sin(ph))]), "red", R=3, folds=True)
    add("helm", "head", ellipse(hdx, hdy, 11, 13.5), "steel", R=10, rim=True)
    add("face", "head", poly([(hdx + 2, hdy - 9), (hdx + 12, hdy - 4), (hdx + 12.5, hdy + 6), (hdx + 6, hdy + 11), (hdx + 2, hdy + 8)]), "steel", R=3, rim=True)
    add("crest", "head", poly([(hdx - 9, hdy - 8), (hdx + 5, hdy - 14), (hdx + 5, hdy - 11), (hdx - 9, hdy - 5)]), "gold", R=1.6, line=False)
    add("slit", "head", rect(round(hdx + 4), round(hdy - 2), 9, 2), [SLIT], R=1, line=False, flat=SLIT)
    add("eye", "head", rect(round(hdx + 10), round(hdy - 2), 2, 2), [GLOW], R=1, line=False, flat=GLOW)
    # near arm + sword (always in front of the body)
    ns = (sx - 1, sy + 3); el2, hand2 = ik(ns, p["nearHand"], 14, 14, 1)
    add("nUp", "near", capsule(ns, el2, 5, 4.4), "steel", R=4, group="nU", rim=True)
    add("nLo", "near", capsule(el2, hand2, 4.4, 4), "steel", R=3.6, group="nL", rim=True)
    add("pauldron", "near", ellipse(sx - 1, sy + 1, 8.5, 7.5), "steel", R=6.5, rim=True)
    a = math.radians(p["ang"]); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    hx2, hy2 = hand2
    tipx, tipy = hx2 + dx * 40, hy2 + dy * 40
    add("grip", "near", capsule((hx2 - dx * 8, hy2 - dy * 8), (hx2 + dx * 2, hy2 + dy * 2), 1.9, 1.9), "brown", R=2)
    add("pommel", "near", ellipse(hx2 - dx * 9, hy2 - dy * 9, 2.8, 2.8), "gold", R=2.8)
    add("blade", "near", poly([(hx2 + dx * 4 + nx * 2.5, hy2 + dy * 4 + ny * 2.5), (tipx, tipy), (hx2 + dx * 4 - nx * 2.5, hy2 + dy * 4 - ny * 2.5)]), "steel", R=2, rim=True)
    add("fuller", "near", capsule((hx2 + dx * 6, hy2 + dy * 6), (hx2 + dx * 30, hy2 + dy * 30), .6, .3), [FULLER], R=1, group="blade", line=False, flat=FULLER)
    add("guard", "near", capsule((hx2 + dx * 3 + nx * 6, hy2 + dy * 3 + ny * 6), (hx2 + dx * 3 - nx * 6, hy2 + dy * 3 - ny * 6), 2.1, 2.1), "gold", R=2)
    add("handN", "near", ellipse(hx2, hy2, 3.8, 3.8), "steel", R=3.6)
    # sword swing smear
    if p["smear"]:
        a0, a1 = map(math.radians, p["smear"]); cxs, cys = sx + 2, sy + 10; pts_o, pts_i = [], []
        for k in range(0, 13):
            aa = a0 + (a1 - a0) * k / 12; ro = 46; ri = ro - 11 * math.sin(math.pi * k / 12) - 1
            pts_o.append((cxs + ro * math.cos(aa), cys + ro * math.sin(aa))); pts_i.append((cxs + ri * math.cos(aa), cys + ri * math.sin(aa)))
        add("smear", "fx", poly(pts_o + pts_i[::-1]), [SMEAR2, SMEAR1], R=3, line=False, flat=None)
    order = {l: i for i, l in enumerate(LAYERS)}
    return sorted(P, key=lambda q: order[q.layer])  # stable: keeps insertion order inside a layer

# ---------- rasteriser ----------
def rasterize(parts):
    owner = [[-1] * W for _ in range(H)]; color = [[None] * W for _ in range(H)]
    for zi, q in enumerate(parts):
        x0, y0 = max(0, int(q.bbox[0]) - 2), max(0, int(q.bbox[1]) - 2); x1, y1 = min(W, int(q.bbox[2]) + 3), min(H, int(q.bbox[3]) + 3)
        bw, bh = x1 - x0, y1 - y0
        if bw <= 0 or bh <= 0: continue
        m = [[bool(q.mask(x0 + x, y0 + y)) for x in range(bw)] for y in range(bh)]
        INF = 1e9; d = [[(INF if m[y][x] else 0) for x in range(bw)] for y in range(bh)]
        for y in range(bh):
            for x in range(bw):
                if m[y][x]:
                    v = d[y][x]
                    if x: v = min(v, d[y][x - 1] + 1)
                    if y: v = min(v, d[y - 1][x] + 1)
                    if x and y: v = min(v, d[y - 1][x - 1] + 1.414)
                    if y and x < bw - 1: v = min(v, d[y - 1][x + 1] + 1.414)
                    d[y][x] = v
        for y in range(bh - 1, -1, -1):
            for x in range(bw - 1, -1, -1):
                if m[y][x]:
                    v = d[y][x]
                    if x < bw - 1: v = min(v, d[y][x + 1] + 1)
                    if y < bh - 1: v = min(v, d[y + 1][x] + 1)
                    if x < bw - 1 and y < bh - 1: v = min(v, d[y + 1][x + 1] + 1.414)
                    if y < bh - 1 and x: v = min(v, d[y + 1][x - 1] + 1.414)
                    d[y][x] = v
        R = q.R
        def hg(x, y):
            if x < 0 or y < 0 or x >= bw or y >= bh or not m[y][x]: return 0
            return R * math.sqrt(max(0, 1 - (1 - min(d[y][x], R) / R) ** 2))
        k = len(q.ramp)
        for y in range(bh):
            for x in range(bw):
                if not m[y][x]: continue
                if q.clip == "ring" and d[y][x] > 1.6: continue
                if q.flat: c = q.flat
                else:
                    gx = (hg(x + 1, y) - hg(x - 1, y)) / 2; gy = (hg(x, y + 1) - hg(x, y - 1)) / 2
                    nl = math.sqrt(gx * gx + gy * gy + 1)
                    v = (-gx * LIGHT[0] - gy * LIGHT[1] + LIGHT[2]) / nl
                    if q.folds: v += 0.34 * math.sin((x0 + x) * 0.62 + (y0 + y) * 0.10 + 1.6 * math.sin((y0 + y) * 0.11 + (x0 + x) * 0.05))
                    idx = max(0, min(k - 1, int((v - 0.18) / 0.80 * (k - 0.01))))
                    if k >= 5 and v > 0.93 and d[y][x] > 1: idx = k - 1
                    c = q.ramp[idx]
                    if q.rim and q.rampname == "steel" and d[y][x] <= 1.5 and (gx * LIGHT[0] + gy * LIGHT[1]) > 0.35 and idx <= 2: c = RIM
                owner[y0 + y][x0 + x] = zi; color[y0 + y][x0 + x] = c
    buckets = {l: {} for l in LAYERS + ["lines", "outline"]}
    for y in range(H):
        for x in range(W):
            o = owner[y][x]
            if o >= 0: buckets[parts[o].layer][(x, y)] = color[y][x]
    for y in range(H):
        for x in range(W):
            o = owner[y][x]
            if o < 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H and owner[yy][xx] >= 0 and parts[owner[yy][xx]].layer not in ("shadow", "fx"):
                        buckets["outline"][(x, y)] = OUTLINE; break
            elif parts[o].line and parts[o].layer not in ("shadow", "fx"):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H:
                        o2 = owner[yy][xx]
                        if o2 > o and parts[o2].line and parts[o2].group != parts[o].group and parts[o2].layer != "fx":
                            buckets["lines"][(x, y)] = parts[o].ramp[0]; break
    return buckets

def palette():
    cols = [c for r in RAMPS.values() for c in r] + [OUTLINE, SHADOW, SLIT, GLOW, RIM, FULLER, SMEAR1, SMEAR2]
    return list(dict.fromkeys(c.lower() for c in cols))

def composite(b):
    img = {}
    for l in LAYERS + ["lines", "outline"]:
        for k, c in b[l].items(): img[k] = c
    return img

def write_png(path, rows):  # rows: list of list of (r,g,b,a)
    h, w = len(rows), len(rows[0]); raw = b"".join(b"\x00" + bytes(v for px in r for v in px) for r in rows)
    def ch(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + ch(b"IDAT", zlib.compress(raw, 6)) + ch(b"IEND", b""))

def sheet(frames, path, scale=2, bg=(214, 220, 232, 255)):
    cols = len(frames); rows = [[bg] * (W * scale * cols) for _ in range(H * scale)]
    for fi, img in enumerate(frames):
        for (x, y), c in img.items():
            rgba = (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
            for yy in range(scale):
                for xx in range(scale): rows[y * scale + yy][(fi * W + x) * scale + xx] = rgba
    write_png(path, rows)

ANIMS = {"idle": (6, [150] * 6), "walk": (8, [100] * 8), "attack": (6, [110, 120, 140, 60, 150, 130])}

if __name__ == "__main__":
    import sys, os
    which = sys.argv[1]; n = ANIMS[which][0]
    frames = [composite(rasterize(build(pose(which, i)))) for i in range(n)]
    d = os.path.dirname(os.path.abspath(__file__))
    if n > 6:
        sheet(frames[:4], os.path.join(d, f"prev_{which}_a.png"), scale=2); sheet(frames[4:], os.path.join(d, f"prev_{which}_b.png"), scale=2)
    else: sheet(frames, os.path.join(d, f"prev_{which}.png"), scale=2)
    print("ok", which, n)
