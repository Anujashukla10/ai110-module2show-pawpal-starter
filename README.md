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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

====================================================
        🐾  PawPal+ — Today's Schedule  🐾
====================================================
  Owner : Jordan
  Budget: 120 min  |  Start: 08:00
====================================================

Daily plan for Biscuit (dog)  [budget: 120 min, start: 08:00]
  08:00 — Medication (5 min) [priority: high]
  08:05 — Feeding (10 min) [priority: high]
  08:15 — Morning walk (30 min) [priority: high]
  08:45 — Teeth brushing (10 min) [priority: medium]
  08:55 — Enrichment toy (15 min) [priority: medium]
  09:10 — Bath (40 min) [priority: low]

  Time used: 110 / 120 min

Plan explanation for Biscuit (Jordan, 120 min available):

  ✓ Medication: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Morning walk: scheduled first — highest priority
  ✓ Teeth brushing: included — fits within remaining time (priority: medium)
  ✓ Enrichment toy: included — fits within remaining time (priority: medium)
  ✓ Bath: included — fits within remaining time (priority: low)

====================================================

Daily plan for Mochi (cat)  [budget: 120 min, start: 08:00]
  08:00 — Litter box (5 min) [priority: high]
  08:05 — Feeding (10 min) [priority: high]
  08:15 — Brush coat (10 min) [priority: medium]
  08:25 — Playtime (15 min) [priority: medium]
  08:40 — Vet check-up (30 min) [priority: low]

  Time used: 70 / 120 min

Plan explanation for Mochi (Jordan, 120 min available):

  ✓ Litter box: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Brush coat: included — fits within remaining time (priority: medium)
  ✓ Playtime: included — fits within remaining time (priority: medium)
  ✓ Vet check-up: included — fits within remaining time (priority: low)

====================================================
  All schedules generated. Have a great day! 🐶🐱
====================================================

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

test_pawpal.py::test_mark_complete_changes_status        PASSED
test_pawpal.py::test_add_task_increases_pet_task_count   PASSED

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting |sort_tasks(), sort_by_time() | Sorts tasks by priority and scheduled time. |
| Filtering |filter_by_priority(), filter_by_recurrence(), filter_by_status(), filter_by_pet() | Filters tasks by priority, recurrence, completion status, or pet. |
| Conflict handling |check_conflicts(), check_cross_pet_conflicts() | Detects overlapping tasks and returns warnings. |
| Recurring tasks |next_occurrence(), mark_task_complete() | Automatically creates the next daily or weekly task when completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Run streamlit run app.py and fill in your name, daily time budget, and start time, then click Save owner.
2. Add a pet (name, species, breed, age) and click Add pet.
3. Add tasks one at a time - set a title, duration, priority, and recurrence, then click Add task. Repeat for each care activity.
4. Click Build Today's Schedule to generate the plan. The table shows each task in time order with its assigned slot.
5. Expand "Why was this plan chosen?" to read the explanation of every included and skipped task.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
