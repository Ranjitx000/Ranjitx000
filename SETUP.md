# Setup

## 1. Create the profile repo
```
gh repo create YOUR_USERNAME --public --clone
cd YOUR_USERNAME
```
Copy everything from this project into it (`scripts/`, `assets/`, `.github/`, `README.md`).

## 2. Swap in your own photo
```
pip install -r scripts/requirements.txt
python scripts/prep_photo.py your-photo.jpg prepped-source.png
python scripts/make_ascii_svg.py prepped-source.png assets/avi-ascii.svg
```
No photo yet? `make_demo_source.py` generates the placeholder robot face used above.

## 3. Edit your info card
Open `scripts/make_info_card.py` and edit the `CONTENT` list, then:
```
python scripts/make_info_card.py assets/info-card.svg
```

## 4. Wire up your real contribution data
```
python scripts/fetch_contributions.py YOUR_USERNAME
python scripts/render_heatmap_svg.py data/contributions.json assets/contrib-heatmap.svg
```

## 5. Turn on the daily refresh
Push to `main`, then trigger `.github/workflows/update-profile-art.yml` once by hand
from the **Actions** tab (`workflow_dispatch`) to confirm it commits a fresh heatmap.
It also re-runs automatically every day at 06:17 UTC.

## Color theme
Everything uses one palette (amber-phosphor CRT rather than GitHub's stock green),
defined at the top of each `scripts/*.py` file:
```
AMBER  = "#ffb400"   # primary
AMBER_DIM = "#7a5615"  # secondary / labels
CYAN   = "#39e6ff"   # rare accent — best-day glow, status dots
BG     = "#0a0908"   # near-black background
```
Change these four values to retheme all three SVGs consistently.
