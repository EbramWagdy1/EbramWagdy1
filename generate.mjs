#!/usr/bin/env node
/**
 * Generates a premium animated contribution heatmap SVG.
 * Full redesign: Neon Cyan/Purple color scheme, gradient BG,
 * scanlines, glow effects, shooting star, matching profile card style.
 *
 * Env vars:
 *   GH_USERNAME  - GitHub login (required)
 *   GH_TOKEN     - GitHub GraphQL token (required)
 *   OUTPUT_PATH  - output file path (default: dist/github-jet.svg)
 */

import fs from "node:fs";
import path from "node:path";

const USERNAME = process.env.GH_USERNAME;
const TOKEN    = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;
const OUTPUT   = process.env.OUTPUT_PATH || "dist/github-jet.svg";

const COLS     = 34;
const ROWS     = 7;
const CELL     = 12;
const GAP      = 3;
const STEP     = CELL + GAP;
const GRID_X   = 28;
const GRID_Y   = 22;
const W        = COLS * STEP + GRID_X * 2;      // ~540
const H        = 210;
const LOOP_DUR = 18;  // seconds per full pass
const MAX_TGTS = 14;

// ── Color palette (matches profile card) ──────────────────────
const BG1       = "#07101F";
const BG2       = "#030810";
const CELL_EMPTY= "#0D1F35";
const CELL_LO   = "#0E3D5C";   // 1-2 contributions
const CELL_MID  = "#0EA5E9";   // 3-5
const CELL_HI   = "#00FFF7";   // 6+
const FLASH_C   = "#C7FBFE";
const BULLET_C  = "#00FFF7";
const BLAST_C   = "#7C3AED";
const STAR_TRAIL= "#A78BFA";
const GRID_LINE = "#0EA5E9";

if (!USERNAME) { console.error("Missing GH_USERNAME"); process.exit(1); }
if (!TOKEN)    { console.error("Missing GH_TOKEN");    process.exit(1); }

const QUERY = `
  query($login: String!) {
    user(login: $login) {
      contributionsCollection {
        contributionCalendar {
          weeks {
            contributionDays {
              date
              contributionCount
              color
            }
          }
        }
      }
    }
  }
`;

async function fetchWeeks() {
  const res = await fetch("https://api.github.com/graphql", {
    method:  "POST",
    headers: { Authorization: `bearer ${TOKEN}`, "Content-Type": "application/json" },
    body:    JSON.stringify({ query: QUERY, variables: { login: USERNAME } }),
  });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data.user.contributionsCollection.contributionCalendar.weeks;
}

function buildCells(weeks) {
  const recent   = weeks.slice(-COLS);
  const padCount = COLS - recent.length;
  const padded   = Array.from({ length: padCount }, () => ({
    contributionDays: Array.from({ length: ROWS }, () => ({
      contributionCount: 0, color: null, date: null,
    })),
  })).concat(recent);

  return padded.flatMap((week, col) =>
    week.contributionDays.map((day, row) => {
      const cnt = day.contributionCount || 0;
      let fill  = CELL_EMPTY;
      if (cnt >= 6) fill = CELL_HI;
      else if (cnt >= 3) fill = CELL_MID;
      else if (cnt >= 1) fill = CELL_LO;
      return {
        col, row,
        x:    GRID_X + col * STEP,
        y:    GRID_Y + row * STEP,
        fill, cnt,
        date: day.date,
      };
    })
  );
}

function pickTargets(cells) {
  return [...cells]
    .filter(c => c.cnt > 0)
    .sort((a, b) => b.cnt - a.cnt)
    .slice(0, MAX_TGTS)
    .sort((a, b) => a.col - b.col || a.row - b.row);
}

// Exact key-time: when is the rocket centre over this column?
// Rocket forward pass: x goes from (GRID_X+5) to (GRID_X+(COLS-1)*STEP+CELL-5) in t=0→0.5
function kt(col, dir) {
  const x0   = GRID_X + 5;                          // JET_X_START
  const x1   = GRID_X + (COLS - 1) * STEP + CELL - 5; // JET_X_END
  const xCol = GRID_X + col * STEP + CELL / 2;      // column centre
  const tFwd = 0.5 * (xCol - x0) / (x1 - x0);      // 0 → 0.5
  const t    = Math.max(0.01, Math.min(0.49, tFwd));
  return dir === "fwd" ? t : 1 - t;
}

function f(n) { return +n.toFixed(4); }

// ── Grid with glow on targets ──────────────────────────────────
function buildGrid(cells, targets) {
  const tset = new Set(targets.map(t => `${t.col}-${t.row}`));
  let out = "";
  for (const c of cells) {
    const isTarget = tset.has(`${c.col}-${c.row}`);
    const rx = 2.5;
    if (!isTarget) {
      out += `<rect x="${f(c.x)}" y="${f(c.y)}" width="${CELL}" height="${CELL}" rx="${rx}" fill="${c.fill}" opacity="0.9"/>\n`;
    } else {
      const tFwd  = kt(c.col, "fwd");
      const tBack = kt(c.col, "bwd");
      const [t1, t2] = [Math.min(tFwd, tBack), Math.max(tFwd, tBack)];
      const dur = 0.007;
      out += `<rect x="${f(c.x)}" y="${f(c.y)}" width="${CELL}" height="${CELL}" rx="${rx}" fill="${c.fill}">` +
        `<animate attributeName="fill" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(t1)};${f(t1+dur)};${f(t2)};${f(t2+dur)};1" ` +
        `values="${c.fill};${c.fill};${FLASH_C};${c.fill};${FLASH_C};${c.fill}"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(t1)};${f(t1+dur)};${f(t2)};${f(t2+dur)};1" ` +
        `values="0.9;0.9;1;0.9;1;0.9"/>` +
        `</rect>\n`;
      // glow ring
      out += `<rect x="${f(c.x-1)}" y="${f(c.y-1)}" width="${CELL+2}" height="${CELL+2}" rx="${rx+1}" ` +
        `fill="none" stroke="${FLASH_C}" stroke-width="1.5" opacity="0">` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(t1)};${f(t1+dur)};${f(t2)};${f(t2+dur)};1" ` +
        `values="0;0;0.9;0;0.9;0"/>` +
        `</rect>\n`;
    }
  }
  return out;
}

// ── Bullets & blasts (purple accent) ──────────────────────────
function buildBulletsBlasts(targets) {
  let bullets = "", blasts = "";
  const PAD_Y = H - 38;
  const dur   = 0.007;
  for (const dir of ["fwd", "bwd"]) {
    const ordered = dir === "fwd" ? targets : [...targets].reverse();
    for (const c of ordered) {
      const t     = kt(c.col, dir);
      const rise  = t - dur * 3;
      const cx    = f(c.x + CELL / 2);
      const targY = f(c.y + CELL / 2);
      bullets += `<circle cx="${cx}" cy="${PAD_Y}" r="2.5" fill="${BULLET_C}">` +
        `<animate attributeName="cy" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(rise)};${f(t)};1" values="${PAD_Y};${PAD_Y};${targY};${targY}"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(rise)};${f(t)};${f(t+dur)};1" values="0;1;1;0;0"/>` +
        `</circle>\n`;
      blasts += `<circle cx="${cx}" cy="${targY}" r="0" fill="none" stroke="${BLAST_C}" stroke-width="2" opacity="0">` +
        `<animate attributeName="r"       dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(t)};${f(t+dur*4)};1" values="0;1;10;10"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${f(t)};${f(t+dur*3)};1" values="0;1;0;0"/>` +
        `</circle>\n`;
    }
  }
  return { bullets, blasts };
}

// ── Twinkling stars ────────────────────────────────────────────
function buildStars() {
  const pts = [
    [6,18,1.3],[6,55,1.8],[6,100,2.2],[6,145,1.6],
    [W-7,22,1.4],[W-7,65,1.9],[W-7,110,1.2],[W-7,158,2.1],
    [40,H-14,1.5],[W/2,H-12,1.8],[W-50,H-14,1.3],
  ];
  return pts.map(([x,y,d]) =>
    `<circle cx="${x}" cy="${y}" r="1.2" fill="#8b949e">` +
    `<animate attributeName="opacity" values="0.15;1;0.15" dur="${d}s" repeatCount="indefinite"/></circle>`
  ).join("\n");
}

// ── Shooting star (meteor) ─────────────────────────────────────
function buildMeteor() {
  const y1 = 8, y2 = H - 50;
  const x1 = W - 20, x2 = 30;
  return `<line x1="${x1}" y1="${y1}" x2="${x1}" y2="${y1}" stroke="${STAR_TRAIL}" stroke-width="1.5" opacity="0">
  <animate attributeName="x1"      values="${x1};${x2}"   dur="1.2s" begin="2s;8.5s" fill="freeze"/>
  <animate attributeName="y1"      values="${y1};${y2}"   dur="1.2s" begin="2s;8.5s" fill="freeze"/>
  <animate attributeName="x2"      values="${x1+30};${x2+30}" dur="1.2s" begin="2s;8.5s" fill="freeze"/>
  <animate attributeName="y2"      values="${y1-8};${y2-8}"   dur="1.2s" begin="2s;8.5s" fill="freeze"/>
  <animate attributeName="opacity" values="0;0.8;0"       dur="1.2s" begin="2s;8.5s" fill="freeze"/>
</line>`;
}

// ── Rocket / Jet ───────────────────────────────────────────────
function buildJet() {
  const jY = H - 42;
  return `<g id="jet">
  <g transform="translate(0,0)">
    <!-- Body -->
    <polygon points="0,-18 9,7 4,4 -4,4 -9,7" fill="#58a6ff" stroke="#1f6feb" stroke-width="0.8"/>
    <!-- Wings -->
    <polygon points="-9,7 -16,14 -4,8" fill="#388bfd"/>
    <polygon points="9,7 16,14 4,8"  fill="#388bfd"/>
    <!-- Cockpit -->
    <circle cx="0" cy="-7" r="2.8" fill="#C7FBFE"/>
    <!-- Engine glow -->
    <ellipse cx="0" cy="9" rx="3" ry="2" fill="#7C3AED" opacity="0.7">
      <animate attributeName="ry" values="2;4;2" dur="0.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.6;1;0.5" dur="0.2s" repeatCount="indefinite"/>
    </ellipse>
    <!-- Flame -->
    <polygon points="-4,8 4,8 0,20" fill="#f0883e">
      <animate attributeName="opacity" values="0.5;1;0.55;1" dur="0.15s" repeatCount="indefinite"/>
      <animate attributeName="points"  values="-4,8 4,8 0,18;-3,8 3,8 0,22;-4,8 4,8 0,16" dur="0.15s" repeatCount="indefinite"/>
    </polygon>
  </g>
  <animateTransform attributeName="transform" type="translate"
    dur="${LOOP_DUR}s" repeatCount="indefinite"
    keyTimes="0;0.5;1"
    values="${GRID_X+5},${jY};${GRID_X + (COLS-1)*STEP + CELL - 5},${jY};${GRID_X+5},${jY}"/>
</g>`;
}

// ── Month labels ───────────────────────────────────────────
function buildLabels(cells) {
  const months  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const seenMonth = new Set();   // track which month-index was already drawn
  const labels = [];
  for (const c of cells) {
    if (!c.date || c.row !== 0) continue;
    const parts = c.date.split("-");
    if (parts.length < 2) continue;
    const mNum = parseInt(parts[1]);
    if (isNaN(mNum) || mNum < 1 || mNum > 12) continue;
    if (!seenMonth.has(mNum)) {
      seenMonth.add(mNum);
      labels.push(`<text x="${f(c.x)}" y="13" font-family="'Courier New',monospace" ` +
        `font-size="9" fill="#334155" letter-spacing="0.5">${months[mNum-1]}</text>`);
    }
  }
  return labels.join("\n");
}

// ── Scanline overlay ───────────────────────────────────────────
function buildScanline() {
  return `<rect x="14" y="-20" width="${W-28}" height="20" opacity="0.2"
  fill="url(#scanGrad)" style="mix-blend-mode:screen" rx="4">
  <animateTransform attributeName="transform" type="translate"
    from="0 0" to="0 ${H+40}" dur="5.0s" repeatCount="indefinite"/>
</rect>`;
}

// ── Full SVG ───────────────────────────────────────────────────
function buildSvg(weeks) {
  const cells   = buildCells(weeks);
  const targets = pickTargets(cells);
  const { bullets, blasts } = buildBulletsBlasts(targets);

  return `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <radialGradient id="bgGrad" cx="40%" cy="30%" r="80%">
    <stop offset="0%"   stop-color="${BG1}"/>
    <stop offset="100%" stop-color="${BG2}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%"   stop-color="${CELL_HI}" stop-opacity="0"/>
    <stop offset="50%"  stop-color="${CELL_HI}" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="${CELL_HI}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="dots" width="15" height="15" patternUnits="userSpaceOnUse">
    <rect width="15" height="1" fill="#0EA5E9" opacity="0.03"/>
  </pattern>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- Background -->
<rect width="${W}" height="${H}" rx="14" fill="url(#bgGrad)"/>
<rect width="${W}" height="${H}" rx="14" fill="url(#dots)"/>

<!-- Border pulse -->
<rect x="1.5" y="1.5" width="${W-3}" height="${H-3}" rx="13"
  fill="none" stroke="${GRID_LINE}" stroke-width="1.2" opacity="0.4">
  <animate attributeName="opacity" values="0.25;0.7;0.25" dur="3s" repeatCount="indefinite"/>
</rect>

<!-- Stars -->
${buildStars()}

<!-- Meteor -->
${buildMeteor()}

<!-- Month labels -->
${buildLabels(cells)}

<!-- Grid -->
<g id="grid" filter="url(#glow)">
${buildGrid(cells, targets)}
</g>

<!-- Bullets -->
<g id="bullets">${bullets}</g>

<!-- Blasts -->
<g id="blasts">${blasts}</g>

<!-- Jet -->
${buildJet()}

<!-- Scanline -->
${buildScanline()}
</svg>`;
}

async function main() {
  console.log(`Fetching contributions for ${USERNAME}...`);
  const weeks = await fetchWeeks();
  const svg   = buildSvg(weeks);
  const out   = path.resolve(OUTPUT);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, svg, "utf8");
  console.log(`Wrote ${out} (${svg.length} bytes)`);
}

main().catch(err => { console.error(err); process.exit(1); });
