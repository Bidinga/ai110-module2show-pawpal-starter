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

## Smarter Scheduling

PawPal+ now includes several small but important scheduling improvements to make daily planning more useful and predictable:

- Sorting: tasks are ordered by start time (earlier first) with priority used as a tie-breaker. Unscheduled tasks are shown after scheduled items.
- Filtering: you can filter tasks by pet name (case-insensitive substring match) and by completion status to focus on what matters now.
- Recurring tasks: daily/weekly recurring tasks are expanded into concrete occurrences for the selected date when generating the daily agenda.
- Conflict detection: lightweight overlap checks return a list of conflicting tasks so the app can warn the user rather than crashing. The scheduler supports both reject-on-conflict and force-add behaviors.

These features are implemented in `pawpal_system.py` (see `ScheduleManager.sort_by_time`, `filter_tasks`, `get_daily_agenda`, and `detect_conflicts_for_task`).
