import json
from pathlib import Path

HEROES_DIR = Path("Heroes")

# load roles
with open("roles.json", "r") as f:
    roles_data = json.load(f)

# list of heroes in the team
team = [
    "Weaver.json",
    "Viper.json",
    "Tidehunter.json",
    "Disruptor.json",
    "Venomancer.json"
]

team_totals = {}

for hero_file in team:
    with open(HEROES_DIR / hero_file, "r") as f:
        hero = json.load(f)

    for role in hero["roles"]:
        if role not in roles_data:
            print(f"[WARN] Unknown role '{role}' in {hero['name']}")
            continue

        for axis, value in roles_data[role].items():
            team_totals[axis] = team_totals.get(axis, 0) + value

# output
print("TEAM TOTALS")
for axis, value in sorted(team_totals.items()):
    print(f"{axis:15}: {value}")