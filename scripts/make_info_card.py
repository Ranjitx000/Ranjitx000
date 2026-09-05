"""
Hand-authored neofetch-style SVG panel. Lines print in one after another like
a boot log, each with a tiny [ok] tick that lands just after the line types.

Edit the CONTENT list below with your own role / stack / highlights.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

AMBER = "#ffb400"
AMBER_DIM = "#7a5615"
CYAN = "#39e6ff"
BG = "#0a0908"
WHITE = "#f5efe0"

TITLE = "Ranjitx000@github"

CONTENT = [
    ("role", "Full-stack Engineer, Developer Tools"),
    ("stack", "TypeScript · Python · Rust · Postgres"),
    ("focus", "Dev-experience tooling & CLI ergonomics"),
    ("now", "Building offline-first sync engines"),
    ("prev", "Infra @ a Series B observability startup"),
    ("highlight", "3x open-source maintainer, 1.2k+ stars"),
    ("uptime", "Shipping in production since 2018"),
]

W, H = 560, 340
PAD_X = 26
LINE_H = 30
TOP = 74
CHAR_W_LABEL = 8.0  # rough monospace width for stagger calc


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    rows = []
    ticks = []
    label_w = max(len(k) for k, _ in CONTENT)

    t = 0.5
    for i, (key, val) in enumerate(CONTENT):
        y = TOP + i * LINE_H
        label = key.rjust(label_w)
        full_len = len(label) + 2 + len(val)
        dur = 0.06 + full_len * 0.014
        begin = round(t, 3)
        end = round(t + dur, 3)

        if STATIC:
            rows.append(
                f'<text x="{PAD_X}" y="{y}" class="line">'
                f'<tspan class="key">{esc(label)}</tspan>'
                f'<tspan class="sep"> :: </tspan>'
                f'<tspan class="val">{esc(val)}</tspan></text>'
            )
        else:
            rows.append(f'''
  <g opacity="0" transform="translate(0, 15)">
    <animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
    <animateTransform attributeName="transform" type="translate" from="0 15" to="0 0" begin="{begin}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
    <text x="{PAD_X}" y="{y}" class="line">
      <tspan class="key">{esc(label)}</tspan><tspan class="sep"> :: </tspan><tspan class="val">{esc(val)}</tspan>
    </text>
  </g>
  <circle cx="{W-34}" cy="{y-5}" r="3.5" fill="{CYAN}" opacity="0" filter="url(#glow)">
    <animate attributeName="opacity" values="0;1;0.4;1" begin="{end}s" dur="1s" fill="freeze"/>
  </circle>''')
        t = end + 0.09

    cursor_y = TOP + len(CONTENT) * LINE_H
    footer_begin = round(t + 0.1, 3)

    style = f'''
    text {{ font-family: 'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace; }}
    .line {{ font-size: 15px; }}
    .key {{ fill: {AMBER_DIM}; }}
    .sep {{ fill: {AMBER_DIM}; }}
    .val {{ fill: {WHITE}; }}
    .title {{ fill: {AMBER}; font-size: 14px; letter-spacing: 0.5px; }}
    .dim {{ fill: {AMBER_DIM}; font-size: 12px; }}
    '''

    dots = f'''
    <circle cx="30" cy="30" r="6" fill="#ff5f57"/>
    <circle cx="50" cy="30" r="6" fill="#febc2e"/>
    <circle cx="70" cy="30" r="6" fill="#28c840"/>
    '''

    body_rows = "".join(rows) if not STATIC else "\n".join(rows)

    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="0.8" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="bgGrad" cx="50%" cy="0%" r="100%">
      <stop offset="0%" stop-color="#181512"/>
      <stop offset="100%" stop-color="{BG}"/>
    </radialGradient>
    <linearGradient id="borderGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{AMBER}" />
      <stop offset="50%" stop-color="{CYAN}" />
      <stop offset="100%" stop-color="{AMBER}" />
      <animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" dur="5s" repeatCount="indefinite"/>
    </linearGradient>
    <style>{style}</style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="url(#bgGrad)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>
  <rect x="0" y="0" width="{W}" height="46" rx="10" fill="#141110" opacity="0.6"/>
  <rect x="0" y="36" width="{W}" height="10" fill="#141110" opacity="0.6"/>
  {dots}
  <text x="{W/2}" y="30" text-anchor="middle" class="title" opacity="0.9" filter="url(#glow)">{TITLE}</text>
  <line x1="0" y1="46" x2="{W}" y2="46" stroke="{AMBER_DIM}" stroke-width="1" opacity="0.5"/>

  <g filter="url(#glow)">
  {body_rows}
  </g>

  <rect x="{PAD_X}" y="{cursor_y-14}" width="9" height="16" fill="{AMBER}" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" dur="1s" begin="{footer_begin}s" repeatCount="indefinite"/>
  </rect>
</svg>'''

    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
