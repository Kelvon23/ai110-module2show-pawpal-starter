# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.



## Features

- **Chronological Sorting** — tasks are sorted by `scheduled_time` using string comparison on zero-padded `HH:MM` values; no parsing needed
- **Conflict Warnings** — pairwise overlap detection flags any two tasks whose time windows intersect, shown as red banners in the UI
- **Priority-Based Scheduling** — daily plan fills available time greedily by priority (high → medium → low), skipping tasks that don't fit
- **Filter by Pet** — multi-pet households can view tasks for a single pet using case-insensitive name matching
- **Filter by Status** — toggle between incomplete and completed tasks
- **Daily/Weekly Recurrence** — marking a recurring task complete auto-creates the next occurrence via `timedelta` (no manual re-entry)
- **Reasoning Explanation** — plain-English summary of how many tasks were scheduled, total time used, and which tasks were skipped and why
- **Live Conflict Check** — conflict detection runs on every task view refresh, not just at schedule generation time

## Smarter Scheduling

Phase 2 added four algorithmic improvements to the scheduler: tasks are now sorted chronologically by `scheduled_time` using a lambda key on zero-padded `"HH:MM"` strings; the task list can be filtered by pet name or completion status to reduce noise for multi-pet households; recurring `"daily"` and `"weekly"` tasks automatically generate their next occurrence (via `timedelta`) the moment they are marked complete, eliminating manual re-entry; and a lightweight pairwise conflict detector warns the owner whenever two tasks overlap the same time window, surfacing the warning in both the terminal and the Streamlit UI without ever crashing the app.

Testing PawPal+:

python -m pytest


Sorting Correctness — confirms sort_by_time returns tasks in chronological order (07:00 → 12:00 → 18:00) and doesn't mutate the original list. Confidence Level Rating - 5 

Recurrence Logic — verifies that completing a daily task creates a new task due tomorrow, weekly creates one due in 7 days, and as_needed returns None with no new task added.  Confidence Level Rating - 4

Conflict Detection — checks that overlapping time windows (including exact same start time) trigger a WARNING, non-overlapping tasks produce no warnings, and already-completed tasks are ignored. Confidence Level Rating - 5 

Edge Cases — a pet with no tasks returns an empty plan, an owner with 0 minutes available schedules nothing, and filtering by a nonexistent pet name returns [] without crashing.
Confidence Level Rating - 3