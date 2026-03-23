#!/usr/bin/env python3
"""
Generate a QR code made out of a mosaic of headshots.
Headshot tiles are procedurally generated with diverse skin tones,
hair colours, and backgrounds – no external image required.

Dark QR modules → darkened headshots
Light QR modules → lightened headshots
"""

import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import qrcode

# ── configuration ────────────────────────────────────────────────────────────
QR_TEXT      = "https://github.com/doublenines/hello-world"
OUTPUT_PATH  = "qr_mosaic.png"
TILE_SIZE    = 42          # pixels per headshot cell in the output
N_TILES      = 300         # unique headshot tiles to generate
BORDER_TILES = 2           # QR quiet-zone width (tiles)
RNG_SEED     = 7

# ── palette pools ─────────────────────────────────────────────────────────────
SKIN_TONES = [
    (255, 219, 172), (240, 194, 150), (224, 172, 105),
    (198, 134,  66), (161,  97,  40), (124,  68,  21),
    ( 90,  50,  20), (255, 228, 196), (210, 180, 140),
    (175, 120,  80),
]
HAIR_COLORS = [
    ( 20,  10,   5), ( 80,  50,  20), (150, 100,  50),
    (200, 160,  80), (240, 210, 130), (230,  70,  70),
    ( 50, 100, 180), ( 40, 160, 100), (160,  80, 160),
    (220, 220, 220), ( 60,  60,  60),
]
EYE_COLORS  = [
    ( 80,  50,  20), ( 50,  80, 160), ( 40, 120,  60),
    ( 90,  60,  40), (160, 130,  80), ( 30,  30,  30),
]
BG_COLORS   = [
    (230, 235, 245), (220, 240, 255), (245, 240, 230),
    (240, 255, 240), (255, 245, 230), (230, 245, 255),
    (245, 230, 245), (255, 255, 255), (210, 225, 240),
]


def rand_color(pool, rng):
    base = list(rng.choice(pool))
    jitter = [max(0, min(255, c + rng.randint(-15, 15))) for c in base]
    return tuple(jitter)


def generate_headshot(size=64, rng=None):
    """Draw a stylised portrait with PIL shapes."""
    if rng is None:
        rng = random.Random()

    s = size
    img  = Image.new("RGB", (s, s), rand_color(BG_COLORS, rng))
    draw = ImageDraw.Draw(img)

    skin = rand_color(SKIN_TONES, rng)
    hair = rand_color(HAIR_COLORS, rng)
    eye  = rand_color(EYE_COLORS,  rng)

    # ── neck ──────────────────────────────────────────────────────────────────
    neck_w = int(s * 0.18)
    neck_x = (s - neck_w) // 2
    draw.rectangle([neck_x, int(s * 0.62), neck_x + neck_w, s], fill=skin)

    # ── shoulders / shirt ─────────────────────────────────────────────────────
    shirt_colors = [(70, 100, 160), (160, 70, 70), (70, 140, 80),
                    (200, 200, 200), (50, 50, 50), (180, 140, 60)]
    shirt = rand_color(shirt_colors, rng)
    pts = [
        (0, s),
        (0, int(s * 0.78)),
        (int(s * 0.28), int(s * 0.68)),
        (int(s * 0.5),  int(s * 0.72)),
        (int(s * 0.72), int(s * 0.68)),
        (s, int(s * 0.78)),
        (s, s),
    ]
    draw.polygon(pts, fill=shirt)

    # ── head (ellipse) ────────────────────────────────────────────────────────
    head_l = int(s * 0.18)
    head_r = int(s * 0.82)
    head_t = int(s * 0.12)
    head_b = int(s * 0.70)
    draw.ellipse([head_l, head_t, head_r, head_b], fill=skin)

    # ── hair style ────────────────────────────────────────────────────────────
    style = rng.randint(0, 4)
    if style == 0:   # short crop
        draw.ellipse([head_l, head_t, head_r, int(s * 0.38)], fill=hair)
    elif style == 1: # long / wavy sides
        draw.ellipse([head_l - 4, head_t, head_r + 4, int(s * 0.62)], fill=hair)
        draw.ellipse([head_l,     head_t, head_r,      int(s * 0.36)], fill=skin)
    elif style == 2: # bun / top-knot
        draw.ellipse([head_l, head_t, head_r, int(s * 0.34)], fill=hair)
        draw.ellipse([int(s*0.38), int(s*0.04), int(s*0.62), int(s*0.20)], fill=hair)
    elif style == 3: # curly afro
        for _ in range(14):
            cx = rng.randint(head_l - 4, head_r + 4)
            cy = rng.randint(head_t - 4, int(s * 0.40))
            r2 = rng.randint(int(s*0.07), int(s*0.14))
            draw.ellipse([cx-r2, cy-r2, cx+r2, cy+r2], fill=hair)
    else:            # bald / stubble
        stubble = tuple(max(0, c - 20) for c in skin)
        draw.ellipse([head_l, head_t, head_r, int(s * 0.30)], fill=stubble)

    # ── eyebrows ──────────────────────────────────────────────────────────────
    brow_y = int(s * 0.37)
    brow_h = max(2, int(s * 0.025))
    brow_dark = tuple(max(0, c - 40) for c in hair)
    draw.rectangle([int(s*0.25), brow_y, int(s*0.43), brow_y + brow_h], fill=brow_dark)
    draw.rectangle([int(s*0.57), brow_y, int(s*0.75), brow_y + brow_h], fill=brow_dark)

    # ── eyes ──────────────────────────────────────────────────────────────────
    ew, eh = int(s * 0.12), int(s * 0.07)
    for ex in [int(s * 0.30), int(s * 0.60)]:
        ey = int(s * 0.42)
        draw.ellipse([ex - ew//2, ey, ex + ew//2, ey + eh*2], fill=(255,255,255))
        draw.ellipse([ex - eh//2 + 1, ey + 2, ex + eh//2, ey + eh*2 - 1], fill=eye)
        draw.ellipse([ex - 2, ey + 4, ex + 2, ey + 8], fill=(10,10,10))

    # ── nose ──────────────────────────────────────────────────────────────────
    nose_skin = tuple(max(0, c - 15) for c in skin)
    nx = s // 2
    ny = int(s * 0.50)
    draw.ellipse([nx - int(s*0.05), ny, nx + int(s*0.05), ny + int(s*0.07)], fill=nose_skin)

    # ── mouth ─────────────────────────────────────────────────────────────────
    lip_color = tuple(max(0, c - 30) for c in skin)
    smile = rng.choice([True, True, True, False])
    mx, my = s // 2, int(s * 0.59)
    mw = int(s * 0.15)
    if smile:
        # arc approximation via short line + upward curve
        for i in range(-mw, mw + 1, 2):
            curve_y = my + int((i / mw) ** 2 * s * 0.04)
            draw.point((mx + i, curve_y), fill=lip_color)
        draw.line([(mx - mw, my), (mx + mw, my)], fill=lip_color, width=max(1, int(s*0.02)))
    else:
        draw.line([(mx - mw, my), (mx + mw, my)], fill=lip_color, width=max(1, int(s*0.02)))

    # optional glasses
    if rng.random() < 0.25:
        g_col = (60, 60, 60)
        for gx in [int(s * 0.30), int(s * 0.60)]:
            gy = int(s * 0.42)
            gr = int(s * 0.09)
            draw.ellipse([gx - gr, gy, gx + gr, gy + int(s*0.12)],
                         outline=g_col, width=max(1, int(s*0.025)))
        draw.line([int(s*0.39), int(s*0.46), int(s*0.50), int(s*0.46)],
                  fill=g_col, width=max(1, int(s*0.02)))

    # soft blur for a photo-like feel
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    return img


def make_dark_tile(tile):
    arr = np.array(tile).astype(float)
    arr = arr * 0.22
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    out = Image.fromarray(arr)
    r, g, b = out.split()
    r = r.point(lambda p: int(p * 0.8))
    b = b.point(lambda p: min(255, int(p * 1.15)))
    return Image.merge("RGB", (r, g, b))


def make_light_tile(tile):
    arr = np.array(tile).astype(float)
    arr = arr * 0.45 + 130
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def generate_qr_matrix(text, border=BORDER_TILES):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.get_matrix()


def build_mosaic(matrix, dark_tiles, light_tiles, rng):
    rows = len(matrix)
    cols = len(matrix[0])
    canvas = Image.new("RGB", (cols * TILE_SIZE, rows * TILE_SIZE), (240, 240, 240))

    for r, row in enumerate(matrix):
        for c, is_dark in enumerate(row):
            pool = dark_tiles if is_dark else light_tiles
            tile = rng.choice(pool).resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
            processed = make_dark_tile(tile) if is_dark else make_light_tile(tile)
            canvas.paste(processed, (c * TILE_SIZE, r * TILE_SIZE))

    return canvas


if __name__ == "__main__":
    rng = random.Random(RNG_SEED)

    print(f"Generating {N_TILES} synthetic headshot tiles…")
    tiles = [generate_headshot(size=80, rng=rng) for _ in range(N_TILES)]

    # Split by average brightness for better contrast pools
    def avg_b(t):
        return np.array(t).mean()

    brightness = [avg_b(t) for t in tiles]
    median_b   = np.median(brightness)
    dark_pool  = [t for t, b in zip(tiles, brightness) if b <= median_b] or tiles
    light_pool = [t for t, b in zip(tiles, brightness) if b >  median_b] or tiles
    print(f"  Dark pool: {len(dark_pool)}, Light pool: {len(light_pool)}")

    print(f"Generating QR code for: {QR_TEXT}")
    matrix = generate_qr_matrix(QR_TEXT)
    print(f"  QR size: {len(matrix[0])} × {len(matrix)} modules")

    print("Building mosaic…")
    mosaic = build_mosaic(matrix, dark_pool, light_pool, rng)
    mosaic.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"Saved → {OUTPUT_PATH}  ({mosaic.width} × {mosaic.height} px)")
