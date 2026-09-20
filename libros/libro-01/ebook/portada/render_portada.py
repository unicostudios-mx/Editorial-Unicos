#!/usr/bin/env python3
"""Portada «La escribana de los dioses» — concepto A+C (Lumen de Archivo).
1600×2560 para Kindle. Salida: portada.png (y preview chico)."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(41)
W, H = 1600, 2560
DIR = Path(__file__).resolve().parent
FONTS = Path("/root/.claude/skills/synced/a8404302-2317-4120-886f-53608372ec96_ec48bdb0-cdfb-4c53-a139-881fd4d1cb0d/canvas-design/canvas-fonts")

INK   = (13, 11, 9)      # negro-tinta
INK2  = (7, 6, 5)
GOLD  = (201, 162, 75)   # oro viejo
GOLDL = (232, 199, 120)  # oro iluminado
AMBER = (232, 161, 60)   # ámbar de llama
LACRE = (122, 32, 28)    # rojo lacre
PAPER = (216, 201, 168)  # papel de trapo

img = Image.new("RGB", (W, H), INK)
px = img.load()

# ---------- 1. fondo: gradiente vertical con temperatura ----------
for y in range(H):
    t = y / H
    r = int(INK[0] + (INK2[0]-INK[0])*t)
    g = int(INK[1] + (INK2[1]-INK[1])*t)
    b = int(INK[2] + (INK2[2]-INK[2])*t)
    for x in range(0, W, 1):
        px[x, y] = (r, g, b)

# ---------- 2. la herida de luz: resplandor ámbar ----------
# el desgarro está en el canto derecho del libro
BOOK_W, BOOK_H = 760, 1060
BX = (W - BOOK_W)//2          # 420
BY = 1150                      # el libro vive bajo el centro óptico
TEAR = (BX + BOOK_W - 8, BY + 300)   # punto del talón arrancado

glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
# resplandor principal (radial, elíptico hacia arriba)
for i in range(140, 0, -1):
    t = i/140
    rx, ry = int(950*t), int(1350*t)
    alpha = int(102 * (1-t)**1.7)
    gd.ellipse([TEAR[0]-rx, TEAR[1]-int(ry*1.25), TEAR[0]+rx, TEAR[1]+int(ry*0.55)], fill=min(255, alpha+int(18*(1-t))))
glow = glow.filter(ImageFilter.GaussianBlur(30))
amber_layer = Image.new("RGB", (W, H), AMBER)
img = Image.composite(Image.blend(img, amber_layer, 0.55), img, glow)

# núcleo caliente junto al desgarro
core = Image.new("L", (W, H), 0)
cd = ImageDraw.Draw(core)
for i in range(60, 0, -1):
    t = i/60
    cd.ellipse([TEAR[0]-int(180*t), TEAR[1]-int(260*t), TEAR[0]+int(180*t), TEAR[1]+int(140*t)],
               fill=int(150*(1-t)**1.4))
core = core.filter(ImageFilter.GaussianBlur(18))
img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), GOLDL), 0.6), img, core)

# ---------- 3. la ciudad que reza con focos ----------
d = ImageDraw.Draw(img, "RGBA")
cols = []
for c in range(26):                      # columnas flojas de ventanas
    cx = random.randint(140, W-140)
    cols.append(cx)
for cx in cols:
    n = random.randint(2, 6)
    base_y = random.randint(180, 980)
    for k in range(n):
        wy = base_y + k*random.randint(34, 58)
        if wy > 1040: break
        # más brillo cuanto más cerca del cono de luz
        dx = abs(cx - TEAR[0]) / W
        dyf = max(0.0, 1 - (TEAR[1]-wy)/1500)
        a = max(0, int(110 * (1-dx) * (0.35+0.65*dyf) * random.uniform(0.4, 1.0)))
        if a < 8: continue
        w_, h_ = random.randint(5, 9), random.randint(9, 16)
        col = (AMBER[0], AMBER[1]+random.randint(-15, 20), AMBER[2]+random.randint(-10, 25), a)
        d.rectangle([cx-w_//2, wy, cx+w_//2, wy+h_], fill=col)

# ---------- 4. el Registro ----------
book = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(book)
R = 26
# sombra del libro
sh = Image.new("L", (W, H), 0)
sd = ImageDraw.Draw(sh)
sd.rounded_rectangle([BX-18, BY+30, BX+BOOK_W+30, BY+BOOK_H+55], radius=R+10, fill=110)
sh = sh.filter(ImageFilter.GaussianBlur(40))
img = Image.composite(Image.new("RGB", (W, H), (2, 2, 2)), img, sh)

# cuerpo de piel: gradiente horizontal hacia la luz (derecha más cálida)
for xx in range(BOOK_W):
    t = xx / BOOK_W
    warm = t**2.2
    col = (int(26 + 70*warm), int(20 + 46*warm), int(15 + 22*warm), 255)
    bd.line([(BX+xx, BY), (BX+xx, BY+BOOK_H)], fill=col)
# recorte redondeado
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([BX, BY, BX+BOOK_W, BY+BOOK_H], radius=R, fill=255)
book.putalpha(mask)
img.paste(book, (0, 0), book)

d = ImageDraw.Draw(img, "RGBA")
# gofrado ciego: doble marco
d.rounded_rectangle([BX+34, BY+34, BX+BOOK_W-34, BY+BOOK_H-34], radius=14, outline=(0, 0, 0, 120), width=3)
d.rounded_rectangle([BX+40, BY+40, BX+BOOK_W-40, BY+BOOK_H-40], radius=12, outline=(228, 190, 110, 46), width=1)
d.rounded_rectangle([BX+58, BY+58, BX+BOOK_W-58, BY+BOOK_H-58], radius=8, outline=(0, 0, 0, 90), width=2)

# lomo a la izquierda: banda + nervios
d.rectangle([BX, BY, BX+64, BY+BOOK_H], fill=(16, 12, 9, 255))
d.line([(BX+64, BY+4), (BX+64, BY+BOOK_H-4)], fill=(0, 0, 0, 160), width=3)
for k in range(5):
    ny = BY + 150 + k*190
    d.rounded_rectangle([BX+8, ny, BX+56, ny+16], radius=8, fill=(24, 18, 13, 255))
    d.line([(BX+8, ny+16), (BX+56, ny+16)], fill=(0, 0, 0, 120), width=2)
# hilo de lacre: una puntada roja en el lomo (el secreto)
d.line([(BX+20, BY+560), (BX+44, BY+560)], fill=LACRE+(255,), width=5)
d.line([(BX+32, BY+548), (BX+32, BY+572)], fill=LACRE+(255,), width=5)

# silueta: rim oscuro que sostiene el libro contra el resplandor
d.rounded_rectangle([BX, BY, BX+BOOK_W, BY+BOOK_H], radius=R, outline=(0, 0, 0, 110), width=3)
d.line([(BX+BOOK_W-1, BY+R), (BX+BOOK_W-1, BY+BOOK_H-R)], fill=(255, 222, 150, 90), width=2)

# canto de páginas a la derecha
EDGE = 26
for xx in range(EDGE):
    t = xx/EDGE
    c = (int(150+60*t), int(135+55*t), int(105+45*t), 255)
    d.line([(BX+BOOK_W-EDGE+xx, BY+14), (BX+BOOK_W-EDGE+xx, BY+BOOK_H-14)], fill=c)
for yy in range(BY+16, BY+BOOK_H-16, 4):    # hojas
    a = random.randint(20, 60)
    d.line([(BX+BOOK_W-EDGE, yy), (BX+BOOK_W-2, yy)], fill=(60, 48, 34, a))

# ---------- 5. el talón arrancado ----------
tx, ty = BX+BOOK_W-6, BY+300
tear_pts = [(tx-2, ty-52), (tx+34, ty-44), (tx+22, ty-28), (tx+42, ty-16),
            (tx+28, ty+2), (tx+46, ty+16), (tx+24, ty+30), (tx+38, ty+46),
            (tx-2, ty+54)]
d.polygon(tear_pts, fill=PAPER+(255,))
d.line(tear_pts, fill=(255, 240, 200, 240), width=3)
# la herida en el canto: hendidura oscura de donde falta la hoja
d.line([(tx-4, ty-50), (tx-4, ty+52)], fill=(30, 22, 14, 220), width=4)
d.line([(tx-8, ty-44), (tx-8, ty+46)], fill=(0, 0, 0, 130), width=2)
# fulgor sobre el talón
halo = Image.new("L", (W, H), 0)
hd = ImageDraw.Draw(halo)
for i in range(40, 0, -1):
    t = i/40
    hd.ellipse([tx-int(120*t)+16, ty-int(150*t), tx+int(140*t)+16, ty+int(120*t)], fill=int(120*(1-t)**1.3))
halo = halo.filter(ImageFilter.GaussianBlur(10))
img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (255, 226, 160)), 0.55), img, halo)

# ---------- 6. tipografía ----------
d = ImageDraw.Draw(img, "RGBA")
italiana = ImageFont.truetype(str(FONTS/"Italiana-Regular.ttf"), 150)
crimson  = ImageFont.truetype(str(FONTS/"CrimsonPro-Regular.ttf"), 62)
sans     = ImageFont.truetype(str(FONTS/"InstrumentSans-Regular.ttf"), 34)

def tracked(draw, xy, text, font, fill, tracking, anchor_center_x=None):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking*(len(text)-1)
    x = (anchor_center_x - total/2) if anchor_center_x else xy[0]
    y = xy[1]
    for ch, w_ in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w_ + tracking
    return total

# cintillo
tracked(d, (0, 168), "LOS CUADERNOS DE LA ESCRIBANA · CUADERNO I", sans, (190, 160, 105, 235), 9, W/2)
d.line([(W/2-70, 246), (W/2+70, 246)], fill=(190, 160, 105, 120), width=2)

# título en tres líneas, iluminado
lines = ["LA ESCRIBANA", "DE LOS", "DIOSES"]
sizes = [150, 96, 190]
ys    = [360, 545, 675]
for ln, sz, yy in zip(lines, sizes, ys):
    f = ImageFont.truetype(str(FONTS/"Italiana-Regular.ttf"), sz)
    # sombra tenue y letra dorada
    tracked(d, (0, yy+4), ln, f, (0, 0, 0, 140), 14, W/2+3)
    tracked(d, (0, yy), ln, f, (235, 205, 135, 255), 14, W/2)

# autor
tracked(d, (0, H-230), "ALBERTONI", crimson, (206, 176, 120, 245), 16, W/2)

# ---------- 7. grano de papel y viñeta ----------
grain = Image.new("L", (W, H))
gp = grain.load()
for y in range(H):
    for x in range(W):
        gp[x, y] = random.randint(0, 22)
img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (255, 250, 240)), 0.06), img, grain)
# fibras del papel de trapo
fd = ImageDraw.Draw(img, "RGBA")
for _ in range(240):
    fx, fy = random.randint(0, W), random.randint(0, H)
    ln = random.randint(6, 26)
    ang = random.uniform(0, math.pi)
    a = random.randint(5, 14)
    fd.line([(fx, fy), (fx+ln*math.cos(ang), fy+ln*math.sin(ang))], fill=(210, 190, 150, a), width=1)
# viñeta
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
for i in range(80):
    t = i/80
    vd.rectangle([int(-W*0.25*(1-t)), int(-H*0.25*(1-t)), int(W*(1+0.25*(1-t))), int(H*(1+0.25*(1-t)))],
                 outline=int(70*(1-t)**2), width=6)
vig = vig.filter(ImageFilter.GaussianBlur(60))
img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, vig.point(lambda v: v//2))

img.save(DIR/"portada.png")
img.resize((400, 640)).save(DIR/"portada-preview.png")
print("OK portada.png", img.size)
