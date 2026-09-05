"""Creates a realistic-looking data/contributions.json for demo purposes.
Replace with real fetch_contributions.py output when wiring up your own repo."""
import json
import random

random.seed(7)
weeks = 53
days = []
total = 0
for w in range(weeks):
    for d in range(7):
        base = random.random()
        # busier on weekdays, occasional bursts (simulate real commit habits)
        weekday = d not in (0, 6)
        p = 0.55 if weekday else 0.25
        if random.random() < p:
            count = int(random.expovariate(1 / 3)) + 1
            count = min(count, 22)
        else:
            count = 0
        days.append(count)
        total += count

best = max(days)
current_streak = 0
for c in reversed(days):
    if c > 0:
        current_streak += 1
    else:
        break

longest = 0
run = 0
for c in days:
    if c > 0:
        run += 1
        longest = max(longest, run)
    else:
        run = 0

data = {
    "weeks": weeks,
    "days": days,
    "total": total,
    "current_streak": current_streak,
    "longest_streak": longest,
    "best_day": best,
}

with open("../data/contributions.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"wrote contributions.json — total={total} longest_streak={longest} best_day={best}")
