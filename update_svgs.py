import os, urllib.request
from pathlib import Path
from html import escape
from PIL import Image, ImageEnhance, ImageOps

# ───────────────────── CONFIG ─────────────────────
USERNAME   = "EbramWagdy1"
FULL_NAME  = "Ebram Wagdy Samy Zaki"
ROLE       = "Flutter Dev | Mobile &amp; IoT"
ORIGIN     = "Cairo, Egypt"
FOCUS      = "Cross-Platform &amp; Embedded"
STATUS     = "Coding · Designing · Shipping"
TOOLCHAIN  = "VS Code · Git · Firebase"
LANG       = "Dart · C/C++ · Python · JS"
FRAMEWORKS = "Flutter · ESP-IDF · Arduino"
PLATFORMS  = "Android · iOS · ESP32"
CLOUD_IOT  = "Firebase · MQTT · REST · OTA"
UI_UX      = "Animations · Pixel-Perfect UI"
EMAIL      = "wagdyebram78@gmail.com"
PORTFOLIO  = "ebramwagdy.online"
LINKEDIN   = "in/ebramwagdy"
GITHUB_U   = "EbramWagdy1"
AVATAR_URL = "https://avatars.githubusercontent.com/u/165323131?v=4"

# ──────── ASCII PORTRAIT (smaller & cleaner) ────────
avatar_path = "avatar.png"
if not os.path.exists(avatar_path):
    urllib.request.urlretrieve(AVATAR_URL, avatar_path)

im = Image.open(avatar_path).convert("RGB")
w0, h0 = im.size
gray = im.crop((int(w0*.06), 0, int(w0*.94), int(h0*.88))).convert("L")
W, H = 62, 42
gray = gray.resize((W, H), Image.Resampling.LANCZOS)
gray = ImageOps.autocontrast(gray, cutoff=2)
gray = ImageEnhance.Contrast(gray).enhance(2.2)
gray = ImageEnhance.Sharpness(gray).enhance(2.5)
CHARS = " .,:;i1tfLCG08@"
portrait = []
for y in range(H):
    row = "".join(CHARS[int(gray.getpixel((x, y)) / 256 * len(CHARS))] for x in range(W))
    portrait.append(row)

tspans = "\n".join(
    f'<tspan x="24" y="{60.0 + i*9.4:.1f}" xml:space="preserve">{escape(row)}</tspan>'
    for i, row in enumerate(portrait)
)

# ─────────── CLIP PATHS (21 lines) ───────────
def clip(i):
    beg = round(0.5 + i * 0.11, 2)
    return (f'<clipPath id="c{i}"><rect x="430" y="{16+i*21:.0f}" '
            f'width="0" height="23">'
            f'<animate attributeName="width" from="0" to="760" '
            f'dur="0.28s" begin="{beg}s" fill="freeze"/>'
            f'</rect></clipPath>')

clips = "".join(clip(i) for i in range(21))

# ─────────── TERMINAL LINE HELPERS ───────────
TX = 450    # text x origin inside right panel

def tline(ci, y, inner):
    return (f'<g clip-path="url(#c{ci})">'
            f'<text x="{TX}" y="{y}" fill="#dbeafe">{inner}</text></g>')

def prompt(ci, y, text):
    return tline(ci, y,
        f'<tspan class="H">{USERNAME}@devos</tspan>'
        f'<tspan class="cc"> ──────────────────────────────────</tspan>')

def section(ci, y, label):
    return tline(ci, y,
        f'<tspan class="A">── {label} </tspan>'
        f'<tspan class="cc">──────────────────────────────────</tspan>')

def info(ci, y, key, val):
    pad = "·" * max(1, 22 - len(key))
    return tline(ci, y,
        f'<tspan class="cc">· </tspan>'
        f'<tspan class="K">{key}</tspan>'
        f'<tspan class="cc"> {pad} </tspan>'
        f'<tspan class="V">{val}</tspan>')

def blank(ci, y):
    return tline(ci, y, '<tspan class="cc"> </tspan>')

ROWS = [
    prompt (0,  36, ""),
    info   (1,  57, "Name",      FULL_NAME),
    info   (2,  78, "Role",      ROLE),
    info   (3,  99, "Origin",    ORIGIN),
    info   (4, 120, "Focus",     FOCUS),
    info   (5, 141, "Status",    STATUS),
    info   (6, 162, "Tools",     TOOLCHAIN),
    blank  (7, 183),
    section(8, 204, "Tech Stack"),
    info   (9, 225, "Lang",      LANG),
    info   (10,246, "Frameworks",FRAMEWORKS),
    info   (11,267, "Platforms", PLATFORMS),
    info   (12,288, "Cloud/IoT", CLOUD_IOT),
    info   (13,309, "UI/UX",     UI_UX),
    blank  (14,330),
    section(15,351, "Contact"),
    info   (16,372, "Mail",      EMAIL),
    info   (17,393, "Portfolio", PORTFOLIO),
    info   (18,414, "LinkedIn",  LINKEDIN),
    info   (19,435, "GitHub",    GITHUB_U),
    tline  (20,456,
        '<tspan class="cc">· </tspan>'
        '<tspan class="V">30 repos | Flutter | IoT | Egypt</tspan>'),
]
TERM = "".join(ROWS)

# ──────────────────── SVG BUILDER ────────────────────
def svg(dark: bool) -> str:
    if dark:
        BG1, BG2   = "#07101F", "#030810"
        AC1, AC2   = "#00FFF7", "#7C3AED"
        AC3        = "#38BDF8"
        BD1, BD2   = "#7C3AED", "#00FFF7"
        SCAN1      = "#00FFF7"; SCANHI = "#C7FBFE"
        KF, VF, CF = "#00FFF7", "#E2E8F0", "#334155"
        HF         = "#A78BFA"
        AF         = "#34D399"
        PF, PO     = "#060C1C", "0.45"
        TB, TBO    = "#060C1C", "0.88"
        DOT        = "#EF4444"
        SOP        = "0.75"
        BLEND      = "screen"
    else:
        BG1, BG2   = "#EEF2FF", "#D9E4FF"
        AC1, AC2   = "#4F46E5", "#7C3AED"
        AC3        = "#0EA5E9"
        BD1, BD2   = "#6D28D9", "#0EA5E9"
        SCAN1      = "#4F46E5"; SCANHI = "#818CF8"
        KF, VF, CF = "#2563EB", "#0F172A", "#94A3B8"
        HF         = "#6D28D9"
        AF         = "#059669"
        PF, PO     = "#FFFFFF", "0.55"
        TB, TBO    = "#FFFFFF", "0.92"
        DOT        = "#DC2626"
        SOP        = "0.30"
        BLEND      = "multiply"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="580" viewBox="0 0 1200 580">
<defs>
  <linearGradient id="aG" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="{AC1}"><animate attributeName="stop-color" values="{AC1};{AC2};{AC3};{AC1}" dur="7s" repeatCount="indefinite"/></stop>
    <stop offset="100%" stop-color="{AC2}"><animate attributeName="stop-color" values="{AC2};{AC3};{AC1};{AC2}" dur="7s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="bG" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%"   stop-color="{BD1}"/>
    <stop offset="100%" stop-color="{BD2}"/>
  </linearGradient>
  <radialGradient id="bg" cx="30%" cy="20%" r="80%">
    <stop offset="0%"   stop-color="{BG1}"/>
    <stop offset="100%" stop-color="{BG2}"/>
  </radialGradient>
  <linearGradient id="sG" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="{SCAN1}" stop-opacity="0"/>
    <stop offset="46%"  stop-color="{SCAN1}" stop-opacity="0.06"/>
    <stop offset="50%"  stop-color="{SCANHI}" stop-opacity="0.65"/>
    <stop offset="54%"  stop-color="{SCAN1}" stop-opacity="0.06"/>
    <stop offset="100%" stop-color="{AC2}"   stop-opacity="0"/>
  </linearGradient>
  <pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{CF}" opacity="0.05"/>
  </pattern>
  <mask id="rev" maskUnits="userSpaceOnUse" x="0" y="0" width="420" height="580">
    <rect x="0" y="0" width="420" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="560" dur="2.0s" begin="0.1s" fill="freeze"/>
    </rect>
  </mask>
  {clips}
  <style>
    text,tspan{{white-space:pre;font-family:'Courier New',Consolas,monospace}}
    .asc{{font-size:8.5px;fill:url(#aG);letter-spacing:-0.1px}}
    .K  {{font-size:15px;fill:{KF};font-weight:bold}}
    .V  {{font-size:15px;fill:{VF}}}
    .cc {{font-size:15px;fill:{CF}}}
    .H  {{font-size:17px;fill:{HF};font-weight:bold}}
    .A  {{font-size:13px;fill:{AF};font-weight:bold;letter-spacing:1px}}
    .tl {{font-size:11px;fill:{CF};letter-spacing:0.4px}}
    .sl {{font-size:8px; fill:{DOT};letter-spacing:2px;font-weight:bold}}
    .pt {{font-size:10px;fill:{AC3};letter-spacing:2.5px;opacity:0.65}}
    .cb {{fill:{AC1}}}
  </style>
</defs>

<!-- BG -->
<rect width="1200" height="580" rx="18" fill="url(#bg)"/>
<rect width="1200" height="580" rx="18" fill="url(#sl)"/>

<!-- Title bar -->
<rect x="3" y="3" width="1194" height="34" rx="16" fill="{TB}" fill-opacity="{TBO}"/>
<circle cx="24" cy="20" r="5" fill="{DOT}"><animate attributeName="opacity" values="1;0.4;1" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="42" cy="20" r="5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.4;1" dur="4s" begin="0.2s" repeatCount="indefinite"/></circle>
<circle cx="60" cy="20" r="5" fill="#10B981"><animate attributeName="opacity" values="1;0.4;1" dur="4s" begin="0.4s" repeatCount="indefinite"/></circle>
<text x="600" y="24" text-anchor="middle" class="tl">{USERNAME}@devos  ─  zsh  ─  ~/profile  ─────────────────────────────────────────────────</text>
<circle cx="1158" cy="20" r="4" fill="{DOT}"><animate attributeName="opacity" values="1;0.1;1" dur="0.9s" repeatCount="indefinite"/></circle>
<text x="1170" y="24" class="sl">LIVE</text>

<g transform="translate(0,38)">

  <!-- Left panel -->
  <rect x="12" y="16" width="400" height="510" rx="12"
        fill="{PF}" fill-opacity="{PO}" stroke="url(#bG)" stroke-width="1.2" opacity="0.5"/>
  <text x="22" y="13" class="pt">[ VISUAL.MAP ]</text>

  <!-- ASCII art -->
  <g mask="url(#rev)">
    <text x="14" y="0" class="asc">
{tspans}
    </text>
  </g>

  <!-- Right panel -->
  <rect x="425" y="4" width="762" height="524" rx="12"
        fill="{PF}" fill-opacity="{PO}" stroke="url(#bG)" stroke-width="1.2" opacity="0.5"/>
  <text x="438" y="13" class="pt">[ SYSTEM.INFO ]</text>

  <!-- Terminal lines -->
  {TERM}

  <!-- Cursor -->
  <rect x="453" y="502" width="8" height="14" class="cb" opacity="0">
    <animate attributeName="opacity"
      values="0;0;1;0;1;0;1;0"
      keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1"
      dur="1.2s" begin="3.0s" repeatCount="indefinite"/>
  </rect>
</g>

<!-- Scan line -->
<rect x="0" y="-70" width="1200" height="70" fill="url(#sG)" opacity="{SOP}"
      style="mix-blend-mode:{BLEND}">
  <animateTransform attributeName="transform" type="translate"
    from="0 -70" to="0 655" dur="3.5s" repeatCount="indefinite"/>
</rect>

<!-- Border pulse -->
<rect x="3" y="3" width="1194" height="574" rx="18"
      fill="none" stroke="url(#bG)" stroke-width="2" opacity="0.6">
  <animate attributeName="opacity" values="0.35;0.8;0.35" dur="2.8s" repeatCount="indefinite"/>
</rect>
</svg>
"""

Path("dark.svg").write_text(svg(True),  encoding="utf-8")
Path("light.svg").write_text(svg(False), encoding="utf-8")
Path("dark-profile.svg").write_text(svg(True),  encoding="utf-8")
Path("light-profile.svg").write_text(svg(False), encoding="utf-8")
print("Done.")
