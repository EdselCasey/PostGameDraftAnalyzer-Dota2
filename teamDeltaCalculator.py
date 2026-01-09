import json
from pathlib import Path
import os

team_a_names = []
team_b_names = []

WEAKNESS_KEYS = [
    "MapCollapseRisk",
    "MapReach",
    "MapLock",
    "LateGame",
    "BurstResilience",
    "CounterEngage",
    "Survivability",
    "ObjectiveConversion",
    "FightPersistence",
    "MidGame"
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
    "sky",
    "ember",
    "bb",
    "sb",
    "axe"
    
]

team_b_names_input = [
   "gyro",
   "lock",
   "bh",
   "beast",
   "tusk"
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



def survivability(delta):
    return (
        delta.get("Durability", 0)
        + delta.get("Control", 0)
        - delta.get("AreaDamage", 0)
        - delta.get("BurstDamage", 0)
        - delta.get("SingleTarget", 0)
        - delta.get("SustainedDamage", 0)
    )

def mid_game(delta):
    return (
        delta.get("Tempo", 0)
        + delta.get("Engagement", 0)
        + delta.get("BurstDamage", 0)
        + 0.5 * delta.get("VisionAccess", 0)
    )


def burst_resilience(delta):
    return (
        delta.get("Durability", 0)
        + 0.5 * delta.get("Control", 0)
        - delta.get("BurstDamage", 0)
        - delta.get("SingleTarget", 0)
    )

def late_game(delta):
    return (
        delta.get("SustainedDamage", 0)
        + delta.get("SingleTarget", 0)
        + 0.5 * delta.get("VisionControl", 0)
        - delta.get("Tempo", 0)
    )

def counter_engage(delta):
    return (
        delta.get("Control", 0)
        + delta.get("AreaDamage", 0)
        + delta.get("VisionControl", 0)
        + 0.5 * delta.get("Durability", 0)
    )

def map_collapse_risk(delta):
    return (
        - delta.get("VisionAccess", 0)
        - 0.5 * delta.get("VisionConversion", 0)
        - delta.get("Survivability", 0)
        + delta.get("AreaDamage", 0)
        + delta.get("SustainedDamage", 0)
    )

def early_game(delta):
    return (
        delta.get("Engagement", 0)
        + delta.get("Control", 0)
        + delta.get("Tempo", 0)
        + 0.75 * delta.get("VisionAccess", 0)
        - 0.5 * delta.get("SustainedDamage", 0)
    )

def objective_conversion(delta):
    return (
        delta.get("Tempo", 0) * 0.5
        + delta.get("SustainedDamage", 0)
        + delta.get("AreaDamage", 0) * 0.5
        + delta.get("VisionConversion", 0)
        + delta.get("VisionControl", 0) * 0.5
    )

def map_reach(delta):
    return (
        delta.get("VisionAccess", 0)
        + 0.5 * delta.get("VisionConversion", 0)
        + 0.5 * delta.get("Engagement", 0)
        + 0.25 * delta.get("Tempo", 0)
        + 0.25 * delta.get("Durability", 0)
    )

def map_lock(delta):
    return (
        delta.get("VisionControl", 0)
        + delta.get("AreaDamage", 0)
        + delta.get("Control", 0)
        + 0.5 * delta.get("Durability", 0)
    )

def fight_persistence(delta):
    return (
        delta.get("SustainedDamage", 0)
        + 0.5 * delta.get("Engagement", 0)
        + 0.5 * delta.get("Control", 0)
        - 2.0 * delta.get("CounterEngage", 0)
        - 0.5 * delta.get("MapLock", 0)
    )


def compute_team_axes(delta):
    return {
        "CounterEngage": counter_engage(delta),
        "LateGame": late_game(delta),
        "EarlyGame": early_game(delta),
        "Survivability": survivability(delta),
        "BurstResilience": burst_resilience(delta),
        "MapReach": map_reach(delta),
        "MapLock": map_lock(delta),
        "MapCollapseRisk": map_collapse_risk(delta),
        "ObjectiveConversion": objective_conversion(delta),
        "FightPersistence": fight_persistence(delta),
        "MidGame": mid_game(delta)
    }


def compare_teams(team_a_files, team_b_files):
    delta = {}

    all_axes = set(team_a_files.keys()) | set(team_b_files.keys())

    for axis in all_axes:
        a_val = team_a_files.get(axis, 0)
        b_val = team_b_files.get(axis, 0)
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
            "MapCollapseRisk": sim_axes["MapCollapseRisk"],
            "LateGame": sim_axes["LateGame"],
            "BurstResilience": sim_axes["BurstResilience"],
            "CounterEngage": sim_axes["CounterEngage"],
            "Survivability": sim_axes["Survivability"],
            "ObjectiveConversion": sim_axes["ObjectiveConversion"],
            "MapReach": sim_axes["MapReach"],
            "MapLock": sim_axes["MapLock"],
            "FightPersistence": sim_axes["FightPersistence"],
            "MidGame": sim_axes["MidGame"]
        }

        # B vs A (for exploitation)
        sim_delta_b = compare_teams(sim_team_b_totals, sim_team_a_totals)
        sim_axes_b = compute_team_axes(sim_delta_b)

        sim_metrics_b = {
            "MapCollapseRisk": sim_axes_b["MapCollapseRisk"],
            "LateGame": sim_axes_b["LateGame"],
            "BurstResilience": sim_axes_b["BurstResilience"],
            "CounterEngage": sim_axes_b["CounterEngage"],
            "Survivability": sim_axes_b["Survivability"],
            "ObjectiveConversion": sim_axes_b["ObjectiveConversion"],
            "MapReach": sim_axes_b["MapReach"],
            "MapLock": sim_axes_b["MapLock"],
            "FightPersistence": sim_axes_b["FightPersistence"],
            "MidGame": sim_axes_b["MidGame"]
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
    "counter_engage": counter_engage(delta),
    "late_game": late_game(delta),
    "early_game": early_game(delta),
    "survivability": survivability(delta),
    "burst_resilience": burst_resilience(delta),
    "map_collapse_risk": map_collapse_risk(delta),
    "objective_conversion":objective_conversion(delta),
    "map_reach":map_reach(delta),
    "map_lock":map_lock(delta),
    "fight_persistence":fight_persistence(delta),
    "mid_game": mid_game(delta)
}

team_b_axes = {
    "counter_engage": counter_engage(delta_b),
    "late_game": late_game(delta_b),
    "early_game": early_game(delta_b),
    "survivability": survivability(delta_b),
    "burst_resilience": burst_resilience(delta_b),
    "map_collapse_risk": map_collapse_risk(delta_b),
    "objective_conversion":objective_conversion(delta_b),
    "map_reach":map_reach(delta_b),
    "map_lock":map_lock(delta_b),
    "fight_persistence":fight_persistence(delta_b),
    "mid_game": mid_game(delta_b)
}

baseline = {
    "MapCollapseRisk": team_axes["map_collapse_risk"],
    "MapReach": team_axes["map_reach"],
    "MapLock": team_axes["map_lock"],
    "LateGame": team_axes["late_game"],
    "BurstResilience": team_axes["burst_resilience"],
    "CounterEngage": team_axes["counter_engage"],
    "Survivability": team_axes["survivability"],
    "ObjectiveConversion":team_axes["objective_conversion"],
    "FightPersistence": team_axes["fight_persistence"],
    "MidGame": team_axes["mid_game"]
}


baseline_b = {
    "MapCollapseRisk": team_b_axes["map_collapse_risk"],
    "MapReach": team_b_axes["map_reach"],
    "MapLock": team_b_axes["map_lock"],
    "LateGame": team_b_axes["late_game"],
    "BurstResilience": team_b_axes["burst_resilience"],
    "CounterEngage": team_b_axes["counter_engage"],
    "Survivability": team_b_axes["survivability"],
    "ObjectiveConversion":team_b_axes["objective_conversion"],
    "FightPersistence": team_b_axes["fight_persistence"],
    "MidGame": team_b_axes["mid_game"]
}


enemy_weaknesses = {k: v for k, v in baseline_b.items() if v < 0}

weaknesses = extract_weaknesses(baseline)

# output
print("\nTEAM A HEROES")
print("-------------")
print(", ".join(team_a_names))
print("")
print("Team A Axes")
print("*************")
for axis, value in sorted(team_axes.items()):
    print(f"{axis:9}: {value}")

print("\nTEAM B HEROES")
print("-------------")
print(", ".join(team_b_names))
print("")
print("Team B Axes")
print("*************")
for axis, value in sorted(team_b_axes.items()):
    print(f"{axis:9}: {value}")

results = recommend_heroes(team_a_files, team_b_files, weaknesses, enemy_weaknesses)

print("WEAKNESSES DETECTED:")
print(weaknesses)

if weaknesses:
    print("\nMODE: PATCHING TEAM A")
elif enemy_weaknesses:
    print("\nMODE: EXPLOITING TEAM B")
else:
    print("\nMODE: STRUCTURALLY OPTIMAL")



print("\nSTRUCTURAL GAP PATCHER")
print("----------------------")
for hero, score in results[:20]:
    print(f"{hero:20} +{score:.2f}") 