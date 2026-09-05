"""
Scrapes your public contribution calendar from
https://github.com/users/<username>/contributions (no API token needed)
and writes data/contributions.json with the raw daily counts plus derived
stats used by render_heatmap_svg.py.
"""
import json
import os
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME") or (sys.argv[1] if len(sys.argv) > 1 else None)
if not USERNAME:
    sys.exit("usage: python fetch_contributions.py <github-username>  (or set GH_USERNAME)")

URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day, td[data-level]")
    days = []
    for cell in cells:
        level = cell.get("data-level")
        count_attr = cell.get("data-count")
        if count_attr is not None:
            days.append(int(count_attr))
        elif level is not None:
            # older markup: no raw count, approximate from level bucket
            days.append(int(level) * 3)

    if not days:
        sys.exit("could not parse contribution cells — GitHub markup may have changed")

    total = sum(days)
    best = max(days)

    current_streak = 0
    for c in reversed(days):
        if c > 0:
            current_streak += 1
        else:
            break

    longest = run = 0
    for c in days:
        if c > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    data = {
        "weeks": len(days) // 7,
        "days": days,
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest,
        "best_day": best,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"wrote data/contributions.json — total={total} longest_streak={longest} best_day={best}")


if __name__ == "__main__":
    main()
