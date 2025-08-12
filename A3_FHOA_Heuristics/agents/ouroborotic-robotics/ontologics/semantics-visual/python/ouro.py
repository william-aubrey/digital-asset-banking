# pip install pillow
from PIL import Image, ImageDraw
import math, random

# ---------- config ----------
OUT_W, OUT_H = 1024, 1024
SS = 4                                  # supersample factor
W, H = OUT_W * SS, OUT_H * SS
BG = (10, 12, 18)                       # deep navy background
GOLD_LIGHT = (254, 203, 95)
GOLD_DARK  = (196, 129, 38)
N_FIGS = 18
RADIUS = int(0.33 * W)
RING_THICK = int(0.012 * W)
SEED = 7
random.seed(SEED)

# ---------- helpers ----------
def lerp(a,b,t): return a + (b-a)*t

def gold_shade(t):
    r = int(lerp(GOLD_DARK[0], GOLD_LIGHT[0], t))
    g = int(lerp(GOLD_DARK[1], GOLD_LIGHT[1], t))
    b = int(lerp(GOLD_DARK[2], GOLD_LIGHT[2], t))
    return (r,g,b)

def _norm(x0, y0, x1, y1):
    """Ensure x1>=x0 and y1>=y0 (Pillow rounded_rectangle requires this)."""
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))

def draw_robot_figure(scale=1.0, tstep=0.0):
    """
    Returns an RGBA image of a stylized walking 'robot-person'.
    tstep in [0,1): walking phase (arms/legs).
    """
    s = int(220 * SS * scale)
    img = Image.new("RGBA", (s, s), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # palette for this figure
    tint = gold_shade(0.55 + 0.25*math.sin(2*math.pi*tstep))
    shadow = (0,0,0,90)

    # convenient coords
    cx, cy = s//2, s//2 + int(0.07*s)

    # walking kinematics (subtle swing)
    leg_a = math.radians(25 * math.sin(2*math.pi*tstep))
    leg_b = math.radians(-25 * math.sin(2*math.pi*tstep))
    arm_a = math.radians(-18 * math.sin(2*math.pi*tstep))
    arm_b = math.radians(18 * math.sin(2*math.pi*tstep))

    # proportions
    head = int(0.22*s)
    body_w, body_h = int(0.26*s), int(0.28*s)
    limb_w = max(SS, int(0.055*s))
    upper = int(0.19*s)
    lower = int(0.22*s)

    # ---- shadow pass ----
    def rr(xy, r): d.rounded_rectangle(_norm(*xy), r, fill=shadow)
    def seg(p1,p2,w): d.line([p1,p2], fill=shadow, width=w)

    off = int(0.03*s)
    # head shadow
    rr([cx-head//2+off, cy-int(0.73*s)+off, cx+head//2+off, cy-int(0.73*s)+head+off], int(0.12*head))
    # body shadow
    rr([cx-body_w//2+off, cy-int(0.52*s)+off, cx+body_w//2+off, cy-int(0.24*s)+off], int(0.2*body_w))
    # limbs shadow
    def limb(theta, up_len, low_len, y0, flip=1):
        x1 = cx + int(math.sin(theta)*up_len)*flip; y1 = y0 + int(math.cos(theta)*up_len)
        x2 = x1 + int(math.sin(theta)*low_len)*flip; y2 = y1 + int(math.cos(theta)*low_len)
        seg((cx+off, y0+off), (x1+off, y1+off), limb_w)
        seg((x1+off, y1+off), (x2+off, y2+off), limb_w)

    y_hip = cy - int(0.22*s)
    y_sho = cy - int(0.46*s)
    limb(leg_a, upper, lower, y_hip,  1)
    limb(leg_b, upper, lower, y_hip, -1)
    limb(arm_a, int(0.17*s), int(0.17*s), y_sho,  1)
    limb(arm_b, int(0.17*s), int(0.17*s), y_sho, -1)

    # ---- figure pass ----
    def rr2(xy, r): d.rounded_rectangle(_norm(*xy), r, fill=tint)
    def seg2(p1,p2,w): d.line([p1,p2], fill=tint, width=w, joint="curve")

    # head + visor
    rr2([cx-head//2, cy-int(0.73*s), cx+head//2, cy-int(0.73*s)+head], int(0.12*head))
    visor = int(0.36*head)
    rr2([cx-head//2+int(0.12*head), cy-int(0.73*s)+int(0.18*head),
         cx-head//2+int(0.12*head)+visor, cy-int(0.73*s)+int(0.18*head)+int(0.52*head)], int(0.12*head))

    # torso
    rr2([cx-body_w//2, cy-int(0.52*s), cx+body_w//2, cy-int(0.24*s)], int(0.2*body_w))
    # (the left/right order above is intentionally reversed to show _norm handles it)

    # legs
    def limb2(theta, up_len, low_len, y0, flip=1):
        x1 = cx + int(math.sin(theta)*up_len)*flip; y1 = y0 + int(math.cos(theta)*up_len)
        x2 = x1 + int(math.sin(theta)*low_len)*flip; y2 = y1 + int(math.cos(theta)*low_len)
        seg2((cx, y0), (x1, y1), limb_w)
        seg2((x1, y1), (x2, y2), limb_w)
        d.ellipse(_norm(x2-limb_w//2, y2-limb_w//2, x2+limb_w//2, y2+limb_w//2), fill=tint)

    limb2(leg_a, upper, lower, y_hip,  1)
    limb2(leg_b, upper, lower, y_hip, -1)

    # arms
    limb2(arm_a, int(0.17*s), int(0.17*s), y_sho,  1)
    limb2(arm_b, int(0.17*s), int(0.17*s), y_sho, -1)

    return img

# ---------- compose ----------
# RGBA canvas to allow alpha compositing
canvas = Image.new("RGBA", (W, H), BG + (255,))
draw = ImageDraw.Draw(canvas)

# subtle ring
cx, cy = W//2, H//2
r0 = RADIUS - RING_THICK//2
r1 = RADIUS + RING_THICK//2
draw.ellipse((cx-r1, cy-r1, cx+r1, cy+r1), outline=(30,35,50), width=RING_THICK)

# place figures
for i in range(N_FIGS):
    t = i / N_FIGS
    ang = t * 2*math.pi
    phase = (t*1.0) % 1.0
    fig = draw_robot_figure(scale=0.95, tstep=phase)
    rot_deg = math.degrees(ang) + 90
    fig = fig.rotate(rot_deg, resample=Image.BICUBIC, expand=True)
    x = cx + int(math.cos(ang) * RADIUS) - fig.width//2
    y = cy + int(math.sin(ang) * RADIUS) - fig.height//2
    canvas.alpha_composite(fig, (x, y))

# downsample + convert to RGB for saving
canvas = canvas.resize((OUT_W, OUT_H), Image.LANCZOS).convert("RGB")
canvas.save("ouroborotic_ring.png")
print("Saved ouroborotic_ring.png")
