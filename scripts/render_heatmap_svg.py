"""
Renders data/contributions.json as a 53x7 heat-gradient calendar (amber -> hot
cyan, not GitHub's stock green) with a diagonal reveal and a pulsing glow on
the single best day.
"""
import json
import sys

DATA = sys.argv[1] if len(sys.argv) > 1 else "../data/contributions.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"

BG = "#0a0908"
AMBER = "#ffb400"
AMBER_DIM = "#7a5615"
CYAN = "#39e6ff"
WHITE = "#f5efe0"

# "heat" ramp: cold/empty -> amber -> hot cyan for the rare big days
PALETTE = ["#171310", "#4a2f10", "#9a5a12", "#ffb400", "#39e6ff"]

BOX = 11
GAP = 3
CELL = BOX + GAP
PAD = 28
LEFT_LABEL = 0

WEEKS = 53
DAYS = 7


def level_for(count, thresholds):
    for i, t in enumerate(thresholds):
        if count <= t:
            return i
    return len(thresholds)


def main():
    with open(DATA) as f:
        data = json.load(f)

    days = data["days"]
    total = data["total"]
    longest = data["longest_streak"]
    current = data["current_streak"]
    best = data["best_day"]

    nonzero = sorted(c for c in days if c > 0)
    if nonzero:
        thresholds = [
            0,
            nonzero[int(len(nonzero) * 0.4)] if nonzero else 1,
            nonzero[int(len(nonzero) * 0.7)] if nonzero else 2,
            max(nonzero[int(len(nonzero) * 0.93)], 1),
        ]
    else:
        thresholds = [0, 1, 2, 3]

    grid_w = WEEKS * CELL
    grid_h = DAYS * CELL
    W = PAD * 2 + grid_w + LEFT_LABEL
    H = PAD + grid_h + 74

    best_idx = days.index(best) if best in days else -1

    boxes = []
    for i, count in enumerate(days):
        w = i // DAYS
        d = i % DAYS
        x = PAD + LEFT_LABEL + w * CELL
        y = PAD + d * CELL
        lvl = level_for(count, thresholds) if count > 0 else 0
        color = PALETTE[lvl]
        delay = round(0.02 * (w + d), 3)
        is_best = (i == best_idx and best > 0)

        extra = ""
        if is_best:
            extra = f'''
      <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" begin="{round(delay+1.2,3)}s" repeatCount="indefinite"/>'''
            boxes.insert(0, f'''
    <rect x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2.5" fill="{color}" opacity="0" filter="url(#glow)">
      <animate attributeName="opacity" values="0;0.8;0" dur="1.5s" begin="{round(delay+1.2,3)}s" repeatCount="indefinite"/>
    </rect>''')

        boxes.append(f'''
    <rect x="{x}" y="{y-14}" width="{BOX}" height="{BOX}" rx="2.5" fill="{color}" opacity="0">
      <animate attributeName="y" from="{y-10}" to="{y}" begin="{delay}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.175 0.885 0.32 1.275"/>
      <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze"/>{extra}
    </rect>''')

    reveal_end = round(0.02 * (WEEKS - 1 + DAYS - 1) + 0.35 + 0.15, 3)

    legend_x = W - PAD - (len(PALETTE) * (BOX + 4)) - 46
    legend_y = PAD + grid_h + 26
    legend_boxes = "".join(
        f'<rect x="{legend_x + 40 + i*(BOX+4)}" y="{legend_y-9}" width="{BOX}" height="{BOX}" rx="2" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )

    stats = f"{total:,} contributions in the last year  ·  current streak {current}d  ·  longest streak {longest}d"

    style = f'''
    text {{ font-family: 'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace; }}
    .stats {{ fill: {WHITE}; font-size: 13px; }}
    .legend {{ fill: {AMBER_DIM}; font-size: 11px; }}
    '''

    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="1.8" result="b"/>
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
      <animateTransform attributeName="gradientTransform" type="rotate" from="360 0.5 0.5" to="0 0.5 0.5" dur="5s" repeatCount="indefinite"/>
    </linearGradient>
    <style>{style}</style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="url(#bgGrad)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="url(#borderGrad)" stroke-width="1.5"/>

  <g filter="url(#glow)">
  {"".join(boxes)}
  </g>

  <text x="{legend_x}" y="{legend_y+4}" class="legend">less</text>
  {legend_boxes}
  <text x="{legend_x + 40 + len(PALETTE)*(BOX+4) + 8}" y="{legend_y+4}" class="legend">more</text>

  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{reveal_end}s" dur="0.6s" fill="freeze"/>
    <text x="{PAD}" y="{legend_y+4}" class="stats">{stats}</text>
  </g>
</svg>'''

    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
