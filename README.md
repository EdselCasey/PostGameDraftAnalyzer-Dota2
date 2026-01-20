## Project Overview - Why I started this project??

This project is a post-game Dota 2 draft analyzer designed to evaluate team compositions based on hero roles and their structural strengths rather than individual performance or in-game execution. It assigns scores to heroes based on the functional roles they fulfill, where each role contributes weighted parameters such as damage profile, control, durability, engagement, vision, and tempo. These values are aggregated from roles → heroes → teams to produce a comparative breakdown of both drafts.

The goal is to help players analyze why a game was difficult or lost by highlighting draft-level structural weaknesses, rather than defaulting to individual blame. In many cases, losses emerge from composition constraints—limited map control, poor engagement tools, or mismatched tempo—well before execution errors occur. This tool is intended to surface those underlying draft dynamics, particularly in the early-to-mid game window, where team identities are first established.

---

## Methodology

This analyzer evaluates drafts after a match has concluded, focusing on the structural strengths and limitations created by team composition rather than in-game execution or player performance.

Hero evaluation is centered on the early-to-mid game identity window (approximately levels 6–10), where draft decisions most strongly influence map control, tempo, vision, and engagement patterns. Late-game scaling and isolated mechanical errors are intentionally out of scope, as they introduce variance that obscures draft-level constraints.

Each hero is assigned one or more functional roles based on intended playstyle and identity rather than situational item builds. These roles contribute weighted attributes representing core capabilities such as damage profile, control, durability, engagement, vision, and tempo.

Team-level scores are derived by aggregating these attributes from roles → heroes → teams, allowing drafts to be compared based on absolute capability as well as relative strengths and weaknesses between opposing lineups.

---

## Role System

This analyzer evaluates heroes through a functional role system that represents how a hero is intended to influence the game during the early-to-mid game window. Roles describe playstyle and battlefield function, not lane assignment or item-specific builds. A hero may fulfill multiple roles simultaneously, and role assignments are based on core identity rather than situational execution.

Each role contributes weighted attributes—such as damage profile, control, durability, engagement, vision, and tempo—which are aggregated at the hero and team levels to surface draft-level strengths and limitations.

For readability, roles are grouped by their primary function. These groupings are organizational only and do not affect scoring.

---

## Core Presence & Combat Roles

**Tank** - 
Provides sustained frontline presence and absorbs pressure and, enabling teammates to operate safely in fights and objectives.

**Bruiser** - 
Balances durability and damage, functioning as a persistent threat that can brawl while remaining difficult to remove.

**Duelist** -
Excels in isolated engagements and skirmishes, pressuring single targets and controlling side-lane or pickoff scenarios.

**Battle Dancer** -
Relies on survivability, sustained area damage, and sustained repositioning within fights to apply pressure while engaging in prolonged exposure.

---

## Engagement & Threat Projection Roles

**Diver** -
Penetrates the backline to disrupt or eliminate high-value targets, often committing deeply to force chaotic engagements.

**Zoner** -
Controls space through area denial, forcing enemy repositioning and constraining movement during fights and objectives.

**Artillery** -
Applies long-range pressure from outside immediate engagement range, shaping fights before full commitment occurs and following up engage with long range damage on compromised targets.

---

## Control, Utility & Fight Manipulation Roles

**Controller** -
Applies reliable crowd control to dictate fight flow, initiations, and disengagements.

**Debuffer** -
Weakens enemy effectiveness through disables, slows, damage amplification, or stat reduction.

**Buffer** -
Enhances allied effectiveness by improving survivability, damage output, or mobility during engagements.

**Save** -
Prevents deaths or disengages allies from losing situations, mitigating burst damage and failed initiations.

---

## Damage Specialization Roles

**Marksman** -
Provides sustained, consistent damage output over time at a ranged distance, particularly effective against objectives, low mobility or stationary enemies in extended fights.

**Nuker** -
Delivers high burst damage in short windows, enabling pickoffs and rapid fight swings.

---

## Map Control & Information Roles

**Scout** -
Provides vision, information, and map awareness, enabling safer movement, better engagements, and objective control.

**Multi-Unit** -
Controls additional units or summons to apply pressure, extend vision, or overwhelm areas of the map.

---

## Objective & Structural Pressure Roles

**Pusher** -
Applies direct pressure to towers and objectives, converting map control and won fights into tangible advantages.

---

## Interpretation Notes

Roles are not mutually exclusive; heroes may contribute to multiple roles with varying intensity.

Role influence is evaluated primarily during the early-to-mid game, where draft identity most strongly shapes outcomes.

The system is designed to highlight structural constraints and advantages, not to judge mechanical execution or decision-making.
