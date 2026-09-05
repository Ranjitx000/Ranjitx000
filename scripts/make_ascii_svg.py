"""
Turns a grayscale portrait into a self-typing ASCII-art SVG styled like an
amber-phosphor CRT terminal (think early IBM monochrome monitors, not the
generic matrix-green look).

Usage:
    python make_ascii_svg.py [source.png] [out.svg]

Defaults to demo-source.png -> avi-ascii.svg
"""
import sys
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "demo-source.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"

# bright -> dark. Leading space keeps flat background silent.
RAMP = " .`:-=+*#%@"

COLS = 92
ROWS = 50  # chars are taller than wide, so fewer rows than a square grid

CHAR_W = 7.2
CHAR_H = 13.5
PAD = 24

AMBER = "#ffb400"
AMBER_DIM = "#7a5615"
CYAN = "#39e6ff"
BG = "#0a0908"


def load_grid(path, cols, rows):
    img = Image.open(path).convert("L")
    img = img.resize((cols, rows))
    px = img.load()
    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            v = px[x, y] / 255.0
            idx = int((1 - v) * (len(RAMP) - 1))
            row.append(RAMP[idx])
        grid.append("".join(row))
    return grid


def esc(c):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


def build_svg(grid):
    w = PAD * 2 + COLS * CHAR_W
    h = PAD * 2 + ROWS * CHAR_H + 40

    rows_svg = []
    total_rows = len(grid)
    stagger = 0.045  # seconds between row starts
    row_dur = 0.5

    for i, row in enumerate(grid):
        y = PAD + i * CHAR_H + CHAR_H
        begin = round(0.4 + i * stagger, 3)
        clip_id = f"clip{i}"
        text = "".join(esc(c) for c in row)
        text_w = COLS * CHAR_W

        rows_svg.append(f'''
    <clipPath id="{clip_id}">
      <rect x="{PAD}" y="{y - CHAR_H + 3}" width="0" height="{CHAR_H}">
        <animate attributeName="width" from="0" to="{text_w}"
                 begin="{begin}s" dur="{row_dur}s" fill="freeze"
                 calcMode="spline" keySplines="0.2 0 0.2 1"/>
      </rect>
    </clipPath>''')

    body = []
    for i, row in enumerate(grid):
        y = PAD + i * CHAR_H + CHAR_H
        clip_id = f"clip{i}"
        text = "".join(esc(c) for c in row)
        body.append(
            f'  <text x="{PAD}" y="{y}" clip-path="url(#{clip_id})" '
            f'class="ascii">{text}</text>'
        )

    last_row_end = round(0.4 + (total_rows - 1) * stagger + row_dur, 3)
    cursor_x = PAD
    cursor_y = PAD + (total_rows - 1) * CHAR_H + CHAR_H - CHAR_H + 3

    footer_y = h - 16

    svg = f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.1" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset="48%" stop-color="{CYAN}" stop-opacity="0.08"/>
      <stop offset="52%" stop-color="{AMBER}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="bgGrad" cx="50%" cy="0%" r="100%">
      <stop offset="0%" stop-color="#181512"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{AMBER}" />
      <stop offset="50%" stop-color="{CYAN}" />
      <stop offset="100%" stop-color="{AMBER}" />
      <animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <style>
      .ascii {{ fill: {AMBER}; font-size: 12.5px; letter-spacing: 0.5px; filter: url(#glow); }}
      .dim {{ fill: {AMBER_DIM}; font-size: 11px; }}
    </style>
  </defs>

  <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="url(#bgGrad)"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>

  <!-- boot flicker -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="{AMBER}" opacity="0">
    <animate attributeName="opacity" values="0;0.12;0;0.06;0" dur="0.5s" begin="0s" fill="freeze"/>
  </rect>

  <!-- ambient scanline sweep, single continuous cue that the terminal is "live" -->
  <rect x="0" y="-{h}" width="{w}" height="{h*2}" fill="url(#scan)">
    <animate attributeName="y" from="-{h}" to="0" dur="6s" begin="{last_row_end}s" repeatCount="indefinite"/>
  </rect>
{"".join(rows_svg)}
{chr(10).join(body)}

  <rect x="{cursor_x}" y="{cursor_y}" width="{CHAR_W-1}" height="{CHAR_H-2}" fill="{AMBER}" opacity="0" filter="url(#glow)">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1"
              dur="1s" begin="{last_row_end}s" repeatCount="indefinite"/>
  </rect>

  <text x="{PAD}" y="{footer_y}" class="dim">[ok] portrait rendered · press any key to continue_</text>
</svg>'''
    return svg


def main():
    grid = load_grid(SRC, COLS, ROWS)
    svg = build_svg(grid)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
