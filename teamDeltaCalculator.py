import json
from pathlib import Path
import os

team_a_names = []
team_b_names = []

WEAKNESS_KEYS = [
    "Survivability"
]

def normalize(text: str) -> str:
    return text.lower().strip()

def resolve_hero(input_name: str):
    key = normalize(input_name)
    return hero_index.get(key)

def resolve_team(team_names):
    resolved = []

    for name in team_names:
        hero = resolve_hero(name)

        if not hero:
            raise ValueError(f"Unknown hero or alias: '{name}'")

        resolved.append(hero)

    return resolved



HEROES_DIR = Path("Heroes")

heroes = []

for filename in os.listdir(HEROES_DIR):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(HEROES_DIR, filename), "r", encoding="utf-8") as f:
        hero = json.load(f)
        hero["_file"] = filename 
        heroes.append(hero)

hero_index = {}

for hero in heroes:

    # main name
    hero_index[normalize(hero["name"])] = hero

    # aliases
    for alias in hero.get("alias", []):
        hero_index[normalize(alias)] = hero


# load roles
with open("roles.json", "r") as f:
    roles_data = json.load(f)

def load_team(hero_files):
    totals = {}
    names = []

    for hero_file in hero_files:
        with open(HEROES_DIR / hero_file, "r") as f:
            hero = json.load(f)

        names.append(hero["name"])

        for role in hero["roles"]:
            if role not in roles_data:
                print(f"[WARN] Unknown role '{role}' in {hero['name']}")
                continue

            for axis, value in roles_data[role].items():
                totals[axis] = totals.get(axis, 0) + value

    return totals, names

# list of heroes in the team
team_a_names_input = [
    "sf","lock","ss","storm","doom"

    
]

team_b_names_input = [
   "kotl","tiny","jak","frog","ta"
]

team_a_heroes = resolve_team(team_a_names_input)
team_b_heroes = resolve_team(team_b_names_input)

team_a_files = [hero["_file"] for hero in team_a_heroes]
team_b_files = [hero["_file"] for hero in team_b_heroes]

team_a_totals = {}
team_b_totals = {}

for hero in team_a_heroes:
    team_a_names.append(hero["name"])

    for role in hero["roles"]:
        if role not in roles_data:
            print(f"[WARN] Unknown role '{role}' in {hero['name']}")
            continue

        for axis, value in roles_data[role].items():
            team_a_totals[axis] = team_a_totals.get(axis, 0) + value

for hero in team_b_heroes:

    team_b_names.append(hero["name"])    

    for role in hero["roles"]:
        if role not in roles_data:
            print(f"[WARN] Unknown role '{role}' in {hero['name']}")
            continue

        for axis, value in roles_data[role].items():
            team_b_totals[axis] = team_b_totals.get(axis, 0) + value



def survivability(team1):
     return (
        team1.get("Durability", 0)
        + team1.get("Control", 0)
        + team1.get("ZoneControl", 0)
    )

def initiation(team1):
     return (
        team1.get("Mobility", 0)
        + team1.get("Reach", 0)
    )

def burst(team1):
     return (
        team1.get("SingleTarget", 0)
        + team1.get("BurstDamage", 0)
    )

def pickoffpotential(team1,teamaxes):
     return (
        team1.get("Catch", 0)
        + team1.get("Burst", 0)
        + team1.get("Reach", 0)
    )

def teamfightstrength(team1):
     return (
        team1.get("AreaDamage", 0)
        + team1.get("SustainedDamage", 0)
        + team1.get("SingleTarget", 0)
        + team1.get("BurstDamage", 0)
    )

def poweracceleration(team1):
     return (
        team1.get("SingleTarget", 0)
        + team1.get("SustainedDamage", 0)
    )

def tempopressure(team1):
    return (
        team1.get("Tempo", 0)
        + team1.get("MapAgency", 0)
    )


def objectivepressure(team1):
    return (
        team1.get("Durability", 0)
        + team1.get("SustainedDamage", 0)
        + team1.get("ZoneControl", 0)
        + team1.get("VisionAccess", 0)
        + team1.get("SingleTargetDamage", 0)
    )

def mapcontrol(team1):
    return (
        team1.get("VisionAccess", 0)
        + team1.get("ZoneControl", 0)
        + team1.get("MapAgency", 0)
    )

def late_game(delta):
    return (
        delta.get("SustainedDamage", 0)
        + delta.get("SingleTarget", 0)
        + 0.5 * delta.get("ZoneControl", 0)
        - delta.get("Tempo", 0)
    )

def early_game(delta):
    return (
        delta.get("Engagement", 0)
        + delta.get("Control", 0)
        + delta.get("Tempo", 0)
        + delta.get("MapReach", 0)
        + delta.get("MapLock", 0)
    )



def compute_team_axes(delta):
    return {
        "LateGame": late_game(delta),
        "EarlyGame": early_game(delta),
        "Survivability": survivability(delta)
    }


def compare_teams(team_a_totals, team_b_totals):
    delta = {}

    all_axes = set(team_a_totals.keys()) | set(team_b_totals.keys())
   
    for axis in all_axes:
        a_val = team_a_totals.get(axis, 0)
        b_val = team_b_totals.get(axis, 0)
        delta[axis] = a_val - b_val
    
    return delta

def extract_weaknesses(metrics, threshold=-5):
    return {k: v for k, v in metrics.items() if v < threshold}


def improvement_score(before, after):
    score = 0.0

    for key, before_val in before.items():
        after_val = after.get(key, before_val)
        score += (after_val - before_val)

    return score

def exploit_score(before_weaknesses, after_metrics):
    score = 0.0
    for key, before_val in before_weaknesses.items():
        after_val = after_metrics.get(key, before_val)
        score += (before_val - after_val)

    return score


def recommend_heroes(team_a_files, team_b_files, weaknesses, enemy_weaknesses):
    recommendations = []

    for hero_path in HEROES_DIR.glob("*.json"):
        hero_file = hero_path.name

        if hero_file in team_a_files or hero_file in team_b_files:
            continue  # already picked

        simulated_team = team_a_files + [hero_file]

        # --- recompute team totals ---
        sim_team_a_totals, _ = load_team(simulated_team)
        sim_team_b_totals, _ = load_team(team_b_files)

        # A vs B
        sim_delta = compare_teams(sim_team_a_totals, sim_team_b_totals)
        sim_axes = compute_team_axes(sim_delta)

        sim_metrics = {
            "Survivability": sim_axes["Survivability"]
        }

        # B vs A (for exploitation)
        sim_delta_b = compare_teams(sim_team_b_totals, sim_team_a_totals)
        sim_axes_b = compute_team_axes(sim_delta_b)

        sim_metrics_b = {
            "Survivability": sim_axes_b["Survivability"]
        }

        # -----------------------------
        # MODE SELECTION
        # -----------------------------
        if weaknesses:
            # PATCH MODE
            score = improvement_score(weaknesses, sim_metrics)

        elif enemy_weaknesses:
            # EXPLOIT MODE
            score = exploit_score(enemy_weaknesses, sim_metrics_b)

        else:
            # STRUCTURALLY STABLE
            score = 0.0

        if score > 0:
            recommendations.append((hero_path.stem, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations




delta = compare_teams(team_a_totals, team_b_totals)
delta_b = compare_teams(team_b_totals, team_a_totals)

team_axes = {
    "survivability": survivability(team_a_totals),
    "initiation": initiation(team_a_totals),
    "burst": burst(team_a_totals),
    "teamfightstrength": teamfightstrength(team_a_totals),
    "poweracceleration": poweracceleration(team_a_totals),
    "tempopressure": tempopressure(team_a_totals),
    "mapcontrol": mapcontrol(team_a_totals),
    "objectivepressure": objectivepressure(team_a_totals)
}

team_b_axes = {
    "survivability": survivability(team_b_totals),
    "initiation": initiation(team_b_totals),
    "burst": burst(team_b_totals),
    "teamfightstrength": teamfightstrength(team_b_totals),
    "poweracceleration": poweracceleration(team_b_totals),
    "tempopressure": tempopressure(team_b_totals),
    "mapcontrol": mapcontrol(team_b_totals),
    "objectivepressure": objectivepressure(team_b_totals)
}

baseline = {
    "Survivability": team_axes["survivability"],

}


baseline_b = {
    "Survivability": team_b_axes["survivability"],
}


enemy_weaknesses = {k: v for k, v in baseline_b.items() if v < 0}

weaknesses = extract_weaknesses(baseline)

# output
print("\nTEAM A HEROES")
print("-------------")
print(", ".join(team_a_names))
print("")
print("Team A Totals")
print("*************")
for axis, value in sorted(team_a_totals.items()):
    print(f"{axis:9}: {value}")
print("")
print("Team A Axes")
print("*************")
for axis, value in sorted(team_axes.items()):
    print(f"{axis:9}: {value}")
print("")
print("Team A Delta")
print("*************")
for axis, value in sorted(delta.items()):
    print(f"{axis:9}: {value}")

print("\nTEAM B HEROES")
print("-------------")
print(", ".join(team_b_names))
print("")
print("Team B Totals")
print("*************")
for axis, value in sorted(team_b_totals.items()):
    print(f"{axis:9}: {value}")
print("")
print("Team B Axes")
print("*************")
for axis, value in sorted(team_b_axes.items()):
    print(f"{axis:9}: {value}")
print("")
print("Team B Delta")
print("*************")
for axis, value in sorted(delta_b.items()):
    print(f"{axis:9}: {value}")
#
#results = recommend_heroes(team_a_files, team_b_files, weaknesses, enemy_weaknesses)
#
#print("WEAKNESSES DETECTED:")
#print(weaknesses)
#
#if weaknesses:#
#    print("\nMODE: PATCHING TEAM A")#
#elif enemy_weaknesses:#
#    print("\nMODE: EXPLOITING TEAM B")#
#else:#
#    print("\nMODE: STRUCTURALLY OPTIMAL")



#print("\nSTRUCTURAL GAP PATCHER")
#print("----------------------")
#for hero, score in results[:20]:
#    print(f"{hero:20} +{score:.2f}") 