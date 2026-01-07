import json
from pathlib import Path

HEROES_DIR = Path("Heroes")

# load roles
with open("roles.json", "r") as f:
    roles_data = json.load(f)

# load hero
with open(HEROES_DIR / "TreantProtector.json", "r") as f:
    hero = json.load(f)

totals = {}

for role in hero["roles"]:
    if role not in roles_data:
        continue

    for axis, value in roles_data[role].items():
        totals[axis] = totals.get(axis, 0) + value

print(hero["name"])
for axis, value in totals.items():
    print(f"{axis:12}: {value}")
