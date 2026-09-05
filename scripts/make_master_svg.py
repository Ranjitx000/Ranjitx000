import json
import sys
import os
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "master-profile.svg"

# Colors
BG = "#080C10"
GREEN = "#00FF88"
GREEN_DIM = "#006633"
GREEN_DARK = "#022b18"
BORDER = "#13382f"
TEXT = "#E0E0E0"
TEXT_DIM = "#888888"

W = 1000
H = 1500

def load_grid(path, cols, rows):
    RAMP = " .`:-=+*#%@"
    if not os.path.exists(path):
        return ["".join(" " for _ in range(cols)) for _ in range(rows)]
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

def build_svg():
    rows_svg = []
    
    # 1. Header
    header = f'''
    <rect x="0" y="0" width="{W}" height="40" fill="#040709" />
    <circle cx="20" cy="20" r="6" fill="#ff5f57"/>
    <circle cx="40" cy="20" r="6" fill="#febc2e"/>
    <circle cx="60" cy="20" r="6" fill="#28c840"/>
    <text x="90" y="25" fill="{TEXT_DIM}" font-size="14">ranjit@github:~</text>
    <text x="{W-20}" y="25" fill="{GREEN}" font-size="14" text-anchor="end">// Code Build Learn Grow Repeat &gt;</text>
    <line x1="0" y1="40" x2="{W}" y2="40" stroke="{BORDER}" stroke-width="1"/>
    '''
    rows_svg.append(header)

    # 2. Hero Section
    # Load ASCII
    ascii_grid = load_grid("scripts/demo-source.png", 40, 20)
    ascii_lines = []
    for i, row in enumerate(ascii_grid):
        text = "".join(esc(c) for c in row)
        ascii_lines.append(f'<text x="30" y="{65 + i*12}" class="ascii" fill="{GREEN}">{text}</text>')
    rows_svg.append("".join(ascii_lines))

    hero_info = f'''
    <text x="300" y="80" fill="{TEXT}" font-size="16">Hi there, I'm</text>
    <text x="300" y="115" fill="{GREEN}" font-size="36" font-weight="bold" letter-spacing="1">RANJIT RAMESH PAWAR_</text>
    <text x="300" y="145" fill="#a080ff" font-size="20">Full Stack Developer</text>
    
    <text x="300" y="190" fill="{TEXT_DIM}" font-size="14">"Turning ideas into real-world solutions</text>
    <text x="300" y="210" fill="{TEXT_DIM}" font-size="14">with clean code and creativity."</text>
    
    <text x="300" y="250" fill="{TEXT_DIM}" font-size="12">📍 India    🧠 Passionate Learner    ☕ Code | Coffee | Consistency</text>
    
    <!-- Link Buttons (Visual) -->
    <rect x="300" y="270" width="100" height="30" rx="5" fill="none" stroke="{BORDER}"/>
    <text x="350" y="290" fill="{TEXT}" font-size="12" text-anchor="middle">GitHub</text>
    
    <rect x="410" y="270" width="100" height="30" rx="5" fill="none" stroke="#0077b5"/>
    <text x="460" y="290" fill="#0077b5" font-size="12" text-anchor="middle">LinkedIn</text>
    
    <rect x="520" y="270" width="100" height="30" rx="5" fill="none" stroke="{BORDER}"/>
    <text x="570" y="290" fill="{TEXT}" font-size="12" text-anchor="middle">Email</text>
    '''
    rows_svg.append(hero_info)
    
    mountain_art = """
      "Better
      Code
      Brighter          (
      Tomorrow"          )
                         *
             /\\
            /  \\      /\\
           /    \\    /  \\
          /      \\  /    \\
         /        \\/      \\
    ====/==========\\=======\\===
    """
    m_lines = mountain_art.split("\\n")
    for i, m in enumerate(m_lines):
        rows_svg.append(f'<text x="750" y="{80 + i*14}" class="ascii" fill="{GREEN}">{esc(m)}</text>')

    # Helper for terminal panel
    def panel(x, y, w, h, title, content):
        return f'''
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{BORDER}"/>
        <text x="{x+15}" y="{y+25}" fill="{GREEN}" font-size="14" font-weight="bold">$ {title}</text>
        {content}
        '''
        
    # 3. Neofetch Panel
    neofetch_content = f'''
    <text x="40" y="410" fill="{TEXT}" font-size="12">Ranjit@Developer</text>
    <line x1="40" y1="420" x2="200" y2="420" stroke="{BORDER}" stroke-dasharray="4"/>
    <text x="40" y="445" fill="#39e6ff" font-size="12">OS       <tspan fill="{TEXT}">: Windows 11</tspan></text>
    <text x="40" y="465" fill="#39e6ff" font-size="12">Host     <tspan fill="{TEXT}">: Developer</tspan></text>
    <text x="40" y="485" fill="#39e6ff" font-size="12">Editor   <tspan fill="{TEXT}">: VS Code</tspan></text>
    <text x="40" y="505" fill="#39e6ff" font-size="12">Frontend <tspan fill="{TEXT}">: React.js</tspan></text>
    <text x="40" y="525" fill="#39e6ff" font-size="12">Backend  <tspan fill="{TEXT}">: Node.js</tspan></text>
    <text x="40" y="545" fill="#39e6ff" font-size="12">Database <tspan fill="{TEXT}">: MongoDB</tspan></text>
    <text x="40" y="565" fill="#39e6ff" font-size="12">Tools    <tspan fill="{TEXT}">: Git, Docker</tspan></text>
    <text x="40" y="585" fill="#39e6ff" font-size="12">Status   <tspan fill="{GREEN}">: ● Always Learning</tspan></text>
    '''
    rows_svg.append(panel(20, 360, 310, 250, "neofetch", neofetch_content))

    # 4. About Me Panel
    about_content = f'''
    <text x="360" y="410" fill="{TEXT}" font-size="12">I'm a Full Stack Developer who loves</text>
    <text x="360" y="430" fill="{TEXT}" font-size="12">building scalable web applications.</text>
    <text x="360" y="450" fill="{TEXT}" font-size="12">I enjoy solving real-world problems,</text>
    <text x="360" y="470" fill="{TEXT}" font-size="12">exploring new technologies, and</text>
    <text x="360" y="490" fill="{TEXT}" font-size="12">creating meaningful digital experiences.</text>
    
    <text x="360" y="530" fill="{GREEN}" font-size="12">🌱 <tspan fill="{TEXT_DIM}">Currently learning System Design</tspan></text>
    <text x="360" y="555" fill="{GREEN}" font-size="12">🚀 <tspan fill="{TEXT_DIM}">Building exciting projects</tspan></text>
    <text x="360" y="580" fill="{GREEN}" font-size="12">🤝 <tspan fill="{TEXT_DIM}">Open to collaboration</tspan></text>
    '''
    rows_svg.append(panel(345, 360, 310, 250, "cat about_me.txt", about_content))

    # 5. Stats Panel
    # Normally we would fetch real stats from GitHub API, but we'll use placeholders for visual parity
    stats_content = f'''
    <circle cx="700" cy="415" r="15" fill="#ffb400" opacity="0.2"/>
    <text x="700" y="420" fill="#ffb400" font-size="16" text-anchor="middle">★</text>
    <text x="730" y="410" fill="{TEXT}" font-size="16" font-weight="bold">42</text>
    <text x="730" y="425" fill="{TEXT_DIM}" font-size="10">Total Stars</text>
    
    <circle cx="700" cy="465" r="15" fill="#39e6ff" opacity="0.2"/>
    <text x="700" y="470" fill="#39e6ff" font-size="16" text-anchor="middle">■</text>
    <text x="730" y="460" fill="{TEXT}" font-size="16" font-weight="bold">25</text>
    <text x="730" y="475" fill="{TEXT_DIM}" font-size="10">Public Repositories</text>
    
    <circle cx="700" cy="515" r="15" fill="#a080ff" opacity="0.2"/>
    <text x="700" y="520" fill="#a080ff" font-size="16" text-anchor="middle">♦</text>
    <text x="730" y="510" fill="{TEXT}" font-size="16" font-weight="bold">312</text>
    <text x="730" y="525" fill="{TEXT_DIM}" font-size="10">Total Contributions</text>
    
    <circle cx="700" cy="565" r="15" fill="#ff5f57" opacity="0.2"/>
    <text x="700" y="570" fill="#ff5f57" font-size="16" text-anchor="middle">♥</text>
    <text x="730" y="560" fill="{TEXT}" font-size="16" font-weight="bold">18</text>
    <text x="730" y="575" fill="{TEXT_DIM}" font-size="10">Current Streak</text>
    
    <line x1="860" y1="400" x2="860" y2="580" stroke="{BORDER}" stroke-dasharray="4"/>
    <text x="880" y="460" fill="{GREEN}" font-size="14">Small</text>
    <text x="880" y="480" fill="{GREEN}" font-size="14">Commits</text>
    <text x="880" y="510" fill="{GREEN}" font-size="14">Big</text>
    <text x="880" y="530" fill="{GREEN}" font-size="14">Progress</text>
    '''
    rows_svg.append(panel(670, 360, 310, 250, "./stats", stats_content))

    # 6. Contributions Panel
    boxes = []
    BOX, GAP, WEEKS, DAYS = 11, 3, 53, 7
    CELL = BOX + GAP
    PAD = 20
    PALETTE = ["#04150d", "#004422", "#008844", "#00cc66", "#00ff88"]
    
    if os.path.exists("data/contributions.json"):
        with open("data/contributions.json") as f:
            data = json.load(f)
        days = data["days"]
        nonzero = sorted(c for c in days if c > 0)
        thresholds = [0, nonzero[int(len(nonzero)*0.4)] if nonzero else 1, nonzero[int(len(nonzero)*0.7)] if nonzero else 2, max(nonzero[int(len(nonzero)*0.93)], 1)] if nonzero else [0, 1, 2, 3]
    else:
        days = [0] * (WEEKS * DAYS)
        thresholds = [0,1,2,3]
        
    for i, count in enumerate(days):
        w_idx = i // DAYS
        d_idx = i % DAYS
        x = 40 + w_idx * CELL
        y = 670 + d_idx * CELL
        lvl = 0
        for ti, t in enumerate(thresholds):
            if count <= t:
                lvl = ti
                break
        else:
            lvl = len(thresholds)
        if count == 0: lvl = 0
        color = PALETTE[lvl]
        boxes.append(f'<rect x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" fill="{color}"/>')

    heatmap_content = "".join(boxes)
    heatmap_content += f'''
    <line x1="840" y1="670" x2="840" y2="760" stroke="{BORDER}" stroke-dasharray="4"/>
    <text x="860" y="685" fill="{TEXT}" font-size="12">Consistency</text>
    <text x="860" y="705" fill="{TEXT}" font-size="12">today</text>
    <text x="860" y="725" fill="{TEXT}" font-size="12">creates</text>
    <text x="860" y="745" fill="{TEXT}" font-size="12">a brighter</text>
    <text x="860" y="765" fill="{TEXT}" font-size="12">tomorrow.</text>
    '''
    rows_svg.append(panel(20, 630, 960, 190, "./contributions", heatmap_content))

    # 7. Tech Stack Panel
    stack_content = f'''
    <text x="60" y="880" fill="#39e6ff" font-size="14" font-weight="bold">Frontend</text>
    <text x="320" y="880" fill="#28c840" font-size="14" font-weight="bold">Backend</text>
    <text x="520" y="880" fill="#ffb400" font-size="14" font-weight="bold">Database</text>
    <text x="720" y="880" fill="#ff5f57" font-size="14" font-weight="bold">Tools &amp; Others</text>
    
    <line x1="280" y1="870" x2="280" y2="950" stroke="{BORDER}" stroke-dasharray="4"/>
    <line x1="490" y1="870" x2="490" y2="950" stroke="{BORDER}" stroke-dasharray="4"/>
    <line x1="680" y1="870" x2="680" y2="950" stroke="{BORDER}" stroke-dasharray="4"/>

    <!-- Placeholder text for icons -->
    <text x="60" y="930" fill="{TEXT}" font-size="12">React   JavaScript  HTML5   CSS3</text>
    <text x="320" y="930" fill="{TEXT}" font-size="12">Node.js   Express   Python</text>
    <text x="520" y="930" fill="{TEXT}" font-size="12">MongoDB   MySQL</text>
    <text x="720" y="930" fill="{TEXT}" font-size="12">Git  GitHub  VS Code  Docker</text>
    '''
    rows_svg.append(panel(20, 840, 960, 130, "./tech-stack", stack_content))

    # 8. Projects Panel
    def proj_card(x, y, title, desc, tag1, tag2, tag3, color):
        return f'''
        <rect x="{x}" y="{y}" width="215" height="150" rx="5" fill="none" stroke="{BORDER}"/>
        <circle cx="{x+20}" cy="{y+25}" r="10" fill="{color}" opacity="0.2"/>
        <text x="{x+40}" y="{y+30}" fill="{color}" font-size="14" font-weight="bold">{title}</text>
        <text x="{x+15}" y="{y+60}" fill="{TEXT}" font-size="11">{desc[0]}</text>
        <text x="{x+15}" y="{y+75}" fill="{TEXT}" font-size="11">{desc[1]}</text>
        <text x="{x+15}" y="{y+90}" fill="{TEXT}" font-size="11">{desc[2]}</text>
        
        <rect x="{x+15}" y="{y+115}" width="80" height="20" rx="3" fill="none" stroke="{color}"/>
        <text x="{x+55}" y="{y+129}" fill="{color}" font-size="10" text-anchor="middle">Live Demo</text>
        
        <rect x="{x+105}" y="{y+115}" width="80" height="20" rx="3" fill="none" stroke="{TEXT_DIM}"/>
        <text x="{x+145}" y="{y+129}" fill="{TEXT}" font-size="10" text-anchor="middle">View Code</text>
        '''
        
    projects_content = f'''
    <text x="960" y="1010" fill="{GREEN_DIM}" font-size="12" text-anchor="end">&gt; Real Projects. Real Learning.</text>
    {proj_card(40, 1030, "AI Interview Bot", ["AI-powered interview", "preparation platform", "with real-time feedback."], "React", "Node", "Mongo", "#a080ff")}
    {proj_card(275, 1030, "E-Commerce App", ["Full-featured e-commerce", "web application with", "secure payment gateway."], "React", "Node", "Mongo", "#28c840")}
    {proj_card(510, 1030, "Task Manager", ["A modern task management", "app to boost productivity", "and organization."], "React", "Express", "Mongo", "#39e6ff")}
    {proj_card(745, 1030, "Chat Application", ["Real-time chat app with", "user authentication", "and live messaging."], "React", "Socket.io", "Mongo", "#ff5f57")}
    '''
    rows_svg.append(panel(20, 990, 960, 220, "./featured-projects", projects_content))

    # 9. Building Panel
    build_content = f'''
    <text x="40" y="1280" fill="{TEXT}" font-size="12">[ ] Advanced React Patterns</text>
    <text x="40" y="1305" fill="{TEXT}" font-size="12">[ ] System Design &amp; Scalability</text>
    <text x="40" y="1330" fill="{TEXT}" font-size="12">[ ] AI Powered Web Applications</text>
    <text x="40" y="1355" fill="{TEXT}" font-size="12">[ ] Contributing to Open Source</text>
    
    <line x1="320" y1="1260" x2="320" y2="1360" stroke="{BORDER}" stroke-dasharray="4"/>
    <text x="380" y="1290" fill="{GREEN}" font-size="14" text-anchor="middle">Progress</text>
    <text x="380" y="1310" fill="{GREEN}" font-size="14" text-anchor="middle">Over</text>
    <text x="380" y="1330" fill="{GREEN}" font-size="14" text-anchor="middle">Perfection</text>
    
    <rect x="340" y="1350" width="100" height="6" rx="3" fill="{GREEN_DARK}"/>
    <rect x="340" y="1350" width="60" height="6" rx="3" fill="{GREEN}"/>
    '''
    rows_svg.append(panel(20, 1230, 470, 160, "./currently-building", build_content))

    # 10. Connect Panel
    connect_content = f'''
    <text x="530" y="1280" fill="{TEXT}" font-size="14" font-weight="bold">Let's Build Something Amazing Together!</text>
    <text x="530" y="1310" fill="{TEXT_DIM}" font-size="12">GitHub: /Ranjitx000</text>
    <text x="530" y="1335" fill="{TEXT_DIM}" font-size="12">LinkedIn: /ranjit-pawar</text>
    <text x="530" y="1360" fill="{TEXT_DIM}" font-size="12">Email: ranjitpawar.dev@gmail.com</text>
    
    <text x="940" y="1340" fill="{GREEN}" font-size="12" text-anchor="end">Open</text>
    <text x="940" y="1355" fill="{GREEN}" font-size="12" text-anchor="end">to new</text>
    <text x="940" y="1370" fill="{GREEN}" font-size="12" text-anchor="end">opportunities!</text>
    '''
    rows_svg.append(panel(510, 1230, 470, 160, "./connect", connect_content))

    # 11. Footer
    footer = f'''
    <line x1="20" y1="1430" x2="250" y2="1430" stroke="{BORDER}" />
    <text x="500" y="1435" fill="{GREEN}" font-size="16" font-weight="bold" letter-spacing="2" text-anchor="middle">« CODE . BUILD . LEARN . GROW . REPEAT »</text>
    <line x1="750" y1="1430" x2="980" y2="1430" stroke="{BORDER}" />
    <text x="980" y="1470" fill="{TEXT_DIM}" font-size="12" text-anchor="end">Thanks for visiting!</text>
    '''
    rows_svg.append(footer)

    style = f'''
    text {{ font-family: 'JetBrains Mono','Fira Code',ui-monospace,Consolas,monospace; }}
    .ascii {{ font-size: 10px; letter-spacing: 1px; white-space: pre; }}
    '''

    svg = f'''<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>{style}</style>
  </defs>
  
  <rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{GREEN_DIM}" stroke-width="1.5"/>
  
  {"".join(rows_svg)}
</svg>'''

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")

if __name__ == "__main__":
    build_svg()
