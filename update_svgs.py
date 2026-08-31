import os
import urllib.request
from pathlib import Path
from html import escape
from PIL import Image, ImageEnhance, ImageOps

# ==============================================================
#  CONFIG — update here only
# ==============================================================
USERNAME        = "EbramWagdy1"
DISPLAY_NAME    = "Ebram Wagdy"
FULL_NAME       = "Ebram Wagdy Samy Zaki"
ROLE            = "Flutter Dev · Mobile & IoT Engineer"
ORIGIN          = "Cairo, Egypt"
FOCUS           = "Cross-Platform & Embedded Systems"
STATUS          = "Coding • Designing • Shipping"
TOOLCHAIN       = "VS Code, Git, Linux, Firebase"
LANG            = "Dart, C/C++, Python, JavaScript"
FRAMEWORKS      = "Flutter, ESP-IDF, Arduino"
PLATFORMS       = "Android, iOS, ESP32, ESP8266"
CLOUD_IOT       = "Firebase, MQTT, REST APIs, OTA"
UI_UX           = "Animations, Pixel-Perfect UI"
EMAIL           = "wagdyebram78@gmail.com"
PORTFOLIO       = "ebramwagdy.online"
LINKEDIN        = "in/ebramwagdy"
FACEBOOK        = "ebram.wagdy.5"
INSTAGRAM       = "ebram_wagdy_"
GITHUB_UNAME    = "EbramWagdy1"
AVATAR_URL      = "https://avatars.githubusercontent.com/u/165323131?v=4"

# ==============================================================
#  1.  ASCII PORTRAIT
# ==============================================================
avatar_path = "avatar.png"
if not os.path.exists(avatar_path):
    urllib.request.urlretrieve(AVATAR_URL, avatar_path)

im = Image.open(avatar_path).convert("RGB")
w0, h0 = im.size
crop = (int(w0*0.06), int(h0*0.00), int(w0*0.94), int(h0*0.90))
gray = im.crop(crop).convert("L")

W, H = 84, 55
gray = gray.resize((W, H), Image.Resampling.LANCZOS)
gray = ImageOps.autocontrast(gray, cutoff=2)
gray = ImageEnhance.Contrast(gray).enhance(2.2)
gray = ImageEnhance.Sharpness(gray).enhance(2.8)
gray = ImageEnhance.Brightness(gray).enhance(1.05)

# Richer character palette for better gradient
CHARS = " .,:;i1tfLCG08@"
portrait = []
for y in range(H):
    row = ""
    for x in range(W):
        v = gray.getpixel((x, y))
        row += CHARS[int(v / 256 * len(CHARS))]
    portrait.append(row)

with open("portrait.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(portrait))

# ==============================================================
#  2.  BUILD TSPANS
# ==============================================================
START_Y = 74.0
STEP_Y  = 8.2
tspans = "\n".join(
    f'<tspan x="30" y="{round(START_Y + i * STEP_Y, 2)}" xml:space="preserve">{escape(row)}</tspan>'
    for i, row in enumerate(portrait)
)

# ==============================================================
#  3.  CLIP PATHS  (22 lines of terminal content)
# ==============================================================
clips = "".join(
    f'<clipPath id="lc{i}"><rect x="500" y="{26.0+i*22:.2f}" width="0" height="24">'
    f'<animate attributeName="width" from="0" to="690" dur="0.32s" begin="{0.6+i*0.10:.2f}s" fill="freeze"/>'
    f'</rect></clipPath>'
    for i in range(22)
)

# ==============================================================
#  4.  TERMINAL LINES  (rich, detailed content)
# ==============================================================
def line(lc, y, content):
    return f'<g clip-path="url(#lc{lc})"><text x="520" y="0" fill="#dbeafe"><tspan x="520" y="{y}" {content}</text></g>'

def head_line(lc, y, text):
    return line(lc, y, f'class="head">{text}</tspan><tspan class="cc"> ─────────────────────────────────────────────────</tspan>')

def info_line(lc, y, key, dots, value):
    return line(lc, y, f'class="cc">· </tspan><tspan class="key">{key}</tspan><tspan class="cc">{dots}</tspan><tspan class="value">{value}</tspan>')

def accent_line(lc, y, text):
    return line(lc, y, f'class="accent">── {text}</tspan><tspan class="cc"> ─────────────────────────────────────────────────</tspan>')

def blank(lc, y):
    return f'<g clip-path="url(#lc{lc})"><text x="520" y="0" fill="#dbeafe"><tspan x="520" y="{y}" class="cc"> </tspan></text></g>'

TERM = "".join([
    head_line  (0,  42, f"{USERNAME}@devos"),
    info_line  (1,  66, "Subject",   " ···················· ", FULL_NAME),
    info_line  (2,  88, "Role",      " ······················· ", ROLE),
    info_line  (3, 110, "Origin",    " ····················· ", ORIGIN),
    info_line  (4, 132, "Focus",     " ······················ ", FOCUS),
    info_line  (5, 154, "Status",    " ·········· ", STATUS),
    info_line  (6, 176, "ToolChain", " ··············· ", TOOLCHAIN),
    blank      (7, 198),
    accent_line(8, 220, "Tech Stack"),
    info_line  (9, 242, "Lang",      " ·················· ", LANG),
    info_line  (10,264, "Frameworks"," ·········· ", FRAMEWORKS),
    info_line  (11,286, "Platforms", " ··········· ", PLATFORMS),
    info_line  (12,308, "Cloud/IoT", " ··········· ", CLOUD_IOT),
    info_line  (13,330, "UI/UX",     " ················· ", UI_UX),
    blank      (14,352),
    accent_line(15,374, "Contact"),
    info_line  (16,396, "Mail",      " ··················· ", EMAIL),
    info_line  (17,418, "Web",       " ···················· ", PORTFOLIO),
    info_line  (18,440, "LinkedIn",  " ··············· ", LINKEDIN),
    info_line  (19,462, "GitHub",    " ················· ", GITHUB_UNAME),
    blank      (20,484),
    line       (21,506, 'class="cc">· </tspan><tspan class="value">⭐ 30 repos · 🎯 Focusing · 🌍 Egypt</tspan>'),
])

# ==============================================================
#  5.  SVG BUILDER
# ==============================================================
def build_svg(dark: bool) -> str:
    # Color tokens
    if dark:
        bg1, bg2       = "#080D1A", "#040912"
        ascii_c1, ascii_c2 = "#00FFF7", "#7C3AED"
        ascii_c3, ascii_c4 = "#38BDF8", "#00FFF7"
        border1, border2, border3 = "#7C3AED", "#00FFF7", "#10B981"
        scan1, scan2   = "#00FFF7", "#7C3AED"
        scan_hi        = "#C7FBFE"
        sl_fill        = "#7DD3FC"
        tb_fill, tb_op = "#060C1C", "0.92"
        panel_fill     = "#060C1C"
        panel_op       = "0.4"
        key_c          = "#00FFF7"
        value_c        = "#F1F5F9"
        cc_c           = "#334155"
        head_c         = "#A78BFA"
        accent_c       = "#34D399"
        cursor_c       = "#00FFF7"
        termbar_c      = "#475569"
        scan_lbl       = "#F87171"
        panel_tc       = "#38BDF8"
        scan_blend     = "screen"
        scan_op        = "0.8"
        tb_dot_fill    = "#EF4444"
    else:
        bg1, bg2       = "#F0F4FF", "#D9E4F5"
        ascii_c1, ascii_c2 = "#4F46E5", "#7C3AED"
        ascii_c3, ascii_c4 = "#0EA5E9", "#4F46E5"
        border1, border2, border3 = "#6D28D9", "#0EA5E9", "#059669"
        scan1, scan2   = "#0EA5E9", "#7C3AED"
        scan_hi        = "#38BDF8"
        sl_fill        = "#334155"
        tb_fill, tb_op = "#FFFFFF", "0.95"
        panel_fill     = "#FFFFFF"
        panel_op       = "0.6"
        key_c          = "#2563EB"
        value_c        = "#0F172A"
        cc_c           = "#94A3B8"
        head_c         = "#6D28D9"
        accent_c       = "#059669"
        cursor_c       = "#0EA5E9"
        termbar_c      = "#64748B"
        scan_lbl       = "#DC2626"
        panel_tc       = "#2563EB"
        scan_blend     = "multiply"
        scan_op        = "0.35"
        tb_dot_fill    = "#F87171"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="640" viewBox="0 0 1240 640">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{ascii_c1}"><animate attributeName="stop-color" values="{ascii_c1};{ascii_c2};{ascii_c3};{ascii_c1}" dur="8s" repeatCount="indefinite"/></stop>
    <stop offset="100%" stop-color="{ascii_c2}"><animate attributeName="stop-color" values="{ascii_c2};{ascii_c3};{ascii_c1};{ascii_c2}" dur="8s" repeatCount="indefinite"/></stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{border1}"/>
    <stop offset="50%" stop-color="{border2}"/>
    <stop offset="100%" stop-color="{border3}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="35%" cy="25%" r="75%">
    <stop offset="0%" stop-color="{bg1}"/>
    <stop offset="100%" stop-color="{bg2}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="{scan1}" stop-opacity="0"/>
    <stop offset="44%"  stop-color="{scan1}" stop-opacity="0.07"/>
    <stop offset="50%"  stop-color="{scan_hi}" stop-opacity="0.7"/>
    <stop offset="56%"  stop-color="{scan1}" stop-opacity="0.07"/>
    <stop offset="100%" stop-color="{scan2}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{sl_fill}" opacity="0.04"/>
  </pattern>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="1240" height="650">
    <rect x="0" y="0" width="1240" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="590" dur="2.4s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
  {clips}
  <style>
    .ascii  {{ font-family: 'Courier New', Consolas, monospace; font-size: 7.2px; fill: url(#asciiGrad); letter-spacing: -0.15px; }}
    .key    {{ font-family: 'Courier New', Consolas, monospace; font-size: 14.5px; fill: {key_c}; font-weight: bold; }}
    .value  {{ font-family: 'Courier New', Consolas, monospace; font-size: 14.5px; fill: {value_c}; }}
    .cc     {{ font-family: 'Courier New', Consolas, monospace; font-size: 14.5px; fill: {cc_c}; }}
    .head   {{ font-family: 'Courier New', Consolas, monospace; font-size: 16px;   fill: {head_c}; font-weight: bold; }}
    .accent {{ font-family: 'Courier New', Consolas, monospace; font-size: 13px;   fill: {accent_c}; font-weight: bold; letter-spacing: 1px; }}
    text, tspan {{ white-space: pre; }}
    .tl   {{ font-family: 'Courier New', Consolas, monospace; font-size: 11.5px; fill: {termbar_c}; letter-spacing: 0.4px; }}
    .sl   {{ font-family: 'Courier New', Consolas, monospace; font-size: 9px;    fill: {scan_lbl}; letter-spacing: 1.5px; font-weight: bold; }}
    .pt   {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px;   fill: {panel_tc}; letter-spacing: 2.5px; opacity: 0.7; }}
    .cb   {{ fill: {cursor_c}; }}
  </style>
</defs>

<!-- Background -->
<rect width="1240" height="640" rx="20" fill="url(#bgGlow)"/>
<rect width="1240" height="640" rx="20" fill="url(#scanlines)"/>

<!-- Title bar -->
<g id="titlebar">
  <rect x="3" y="3" width="1234" height="36" rx="18" fill="{tb_fill}" fill-opacity="{tb_op}"/>
  <circle cx="26" cy="21" r="5.5" fill="{tb_dot_fill}"><animate attributeName="opacity" values="1;0.5;1" dur="4.5s" repeatCount="indefinite"/></circle>
  <circle cx="45" cy="21" r="5.5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.5;1" dur="4.5s" begin="0.25s" repeatCount="indefinite"/></circle>
  <circle cx="64" cy="21" r="5.5" fill="#10B981"><animate attributeName="opacity" values="1;0.5;1" dur="4.5s" begin="0.5s" repeatCount="indefinite"/></circle>
  <text x="620" y="26" text-anchor="middle" class="tl">{USERNAME}@devos ─ zsh ─ ~/profile.sh ──live──────────────────────────</text>
  <circle cx="1190" cy="21" r="4" fill="{scan_lbl}"><animate attributeName="opacity" values="1;0.12;1" dur="1.0s" repeatCount="indefinite"/></circle>
  <text x="1200" y="26" class="sl">LIVE</text>
</g>

<g transform="translate(0,42)">
  <!-- Panels -->
  <rect x="14" y="22" width="505" height="498" rx="14" fill="{panel_fill}" fill-opacity="{panel_op}" stroke="url(#borderGrad)" stroke-width="1.2" opacity="0.4"/>
  <rect x="530" y="8"  width="695" height="512" rx="14" fill="{panel_fill}" fill-opacity="{panel_op}" stroke="url(#borderGrad)" stroke-width="1.2" opacity="0.4"/>
  <text x="28"  y="20" class="pt">[ VISUAL.MAP ]</text>
  <text x="545" y="20" class="pt">[ SYSTEM.INFO ]</text>

  <!-- ASCII portrait -->
  <g mask="url(#reveal)">
    <text x="28" y="0" class="ascii">

{tspans}

    </text>
  </g>

  <!-- Terminal content -->
  {TERM}

  <!-- Blinking cursor -->
  <rect x="543" y="492" width="9" height="16" class="cb" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0;1;0;1;0" keyTimes="0;0.01;0.02;0.3;0.5;0.7;0.85;1" dur="1.3s" begin="3.5s" repeatCount="indefinite"/>
  </rect>
</g>

<!-- Scan line -->
<rect x="0" y="-70" width="1240" height="70" fill="url(#scanGrad)" opacity="{scan_op}" style="mix-blend-mode:{scan_blend}">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 715" dur="4.0s" repeatCount="indefinite"/>
</rect>

<!-- Border glow -->
<rect x="3" y="3" width="1234" height="634" rx="18" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.75">
  <animate attributeName="opacity" values="0.45;0.9;0.45" dur="3.0s" repeatCount="indefinite"/>
</rect>
</svg>
"""

dark_svg  = build_svg(dark=True)
light_svg = build_svg(dark=False)

Path("dark.svg").write_text(dark_svg,  encoding="utf-8")
Path("light.svg").write_text(light_svg, encoding="utf-8")
Path("dark-profile.svg").write_text(dark_svg,  encoding="utf-8")
Path("light-profile.svg").write_text(light_svg, encoding="utf-8")
print("All SVGs generated successfully!")
