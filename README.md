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
pip install tabulate        # CLI table formatting
```

### Run the app
```bash
streamlit run app.py
```

### Run from the terminal
```bash
python main.py
```

## 🖥️ Sample Output

```
════════════════════════════════════════════════════════════
               🐾  PawPal+ — Today's Schedule
════════════════════════════════════════════════════════════
  📅  Wednesday, June 24 2026

  Owner:  Jordan
  Budget: 120 min  │  Start: 08:00
════════════════════════════════════════════════════════════

🐕 Biscuit (Golden Retriever)
────────────────────────────────────────────────────────────
╭─────────────┬──────────────────┬────────────┬────────────┬──────────────╮
│ Time        │ Task             │   Duration │ Priority   │ Recurrence   │
├─────────────┼──────────────────┼────────────┼────────────┼──────────────┤
│ 08:00–08:05 │ 💊 Medication     │      5 min │ ● HIGH     │ 📅 daily      │
│ 08:05–08:15 │ 🍽 Feeding        │     10 min │ ● HIGH     │ 📅 daily      │
│ 08:15–08:45 │ 🚶 Morning walk   │     30 min │ ● HIGH     │ 📅 daily      │
│ 08:45–08:55 │ 🛁 Teeth brushing │     10 min │ ● MED      │ 📅 daily      │
│ 08:55–09:10 │ 🎾 Enrichment toy │     15 min │ ● MED      │ 📅 daily      │
│ 09:10–09:50 │ 🛁 Bath           │     40 min │ ● LOW      │ 📆 weekly     │
╰─────────────┴──────────────────┴────────────┴────────────┴──────────────╯

  Time used: [███████████████████████████░░░] 110/120 min

  Progress: 0/6 tasks complete (0%)
  Still to do:
    ○  💊 Medication  @ 08:00
    ○  🍽 Feeding  @ 08:05
    ○  🚶 Morning walk  @ 08:15
    ○  🛁 Teeth brushing  @ 08:45
    ○  🎾 Enrichment toy  @ 08:55
    ○  🛁 Bath  @ 09:10

🐈 Mochi (Siamese)
────────────────────────────────────────────────────────────
╭─────────────┬────────────────┬────────────┬────────────┬──────────────╮
│ Time        │ Task           │   Duration │ Priority   │ Recurrence   │
├─────────────┼────────────────┼────────────┼────────────┼──────────────┤
│ 08:00–08:05 │ 🧹 Litter box   │      5 min │ ● HIGH     │ 📅 daily      │
│ 08:05–08:15 │ 🍽 Feeding      │     10 min │ ● HIGH     │ 📅 daily      │
│ 08:15–08:25 │ 🛁 Brush coat   │     10 min │ ● MED      │ 📆 weekly     │
│ 08:25–08:40 │ 🎾 Playtime     │     15 min │ ● MED      │ 📅 daily      │
│ 08:40–09:10 │ 🏥 Vet check-up │     30 min │ ● LOW      │ 🔔 as needed  │
╰─────────────┴────────────────┴────────────┴────────────┴──────────────╯

  Time used: [█████████████████░░░░░░░░░░░░░] 70/120 min

  Progress: 0/5 tasks complete (0%)
  Still to do:
    ○  🧹 Litter box  @ 08:00
    ○  🍽 Feeding  @ 08:05
    ○  🛁 Brush coat  @ 08:15
    ○  🎾 Playtime  @ 08:25
    ○  🏥 Vet check-up  @ 08:40

⚠️  Conflict Check
────────────────────────────────────────────────────────────
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Medication' (08:00–08:05) overlaps Mochi·'Litter box' (08:00–08:05)
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Feeding' (08:05–08:15) overlaps Mochi·'Feeding' (08:05–08:15)
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Morning walk' (08:15–08:45) overlaps Mochi·'Brush coat' (08:15–08:25)

💡 Why was this plan chosen?
────────────────────────────────────────────────────────────
Plan explanation for Biscuit (Jordan, 120 min available):

  ✓ Medication: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Morning walk: scheduled first — highest priority
  ✓ Teeth brushing: included — fits within remaining time (priority: medium)
  ✓ Enrichment toy: included — fits within remaining time (priority: medium)
  ✓ Bath: included — fits within remaining time (priority: low)

Plan explanation for Mochi (Jordan, 120 min available):

  ✓ Litter box: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Brush coat: included — fits within remaining time (priority: medium)
  ✓ Playtime: included — fits within remaining time (priority: medium)
  ✓ Vet check-up: included — fits within remaining time (priority: low)

════════════════════════════════════════════════════════════
  All schedules generated.  11 tasks · 180 min planned  🐶🐱
════════════════════════════════════════════════════════════
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Task sorting** | `sort_tasks()`, `sort_by_time()` | `sort_tasks()` orders by priority score descending (high=3, medium=2, low=1), then duration ascending as a tiebreaker. `sort_by_time()` re-orders the built plan chronologically using zero-padded `"HH:MM"` string comparison. |
| **Filtering** | `filter_by_priority()`, `filter_by_recurrence()`, `filter_by_status()`, `filter_by_pet()` | Filters tasks by priority level, recurrence pattern, completion status, or pet name. `filter_by_status()` drives the to-do/done metric tiles in the UI. |
| **Conflict handling** | `check_conflicts()`, `check_cross_pet_conflicts()` | Detects overlapping tasks using the interval overlap formula `a_start < b_end and b_start < a_end`. Returns plain warning strings — never raises. Cross-pet detection catches cases where one owner cannot do two things simultaneously. |
| **Recurring tasks** | `next_occurrence()`, `mark_task_complete()` | Uses `datetime.timedelta` to compute next due dates (`+1 day` daily, `+7 days` weekly). Auto-registers the next occurrence in `pet._tasks` when a task is marked complete. `as_needed` tasks return `None`. |
| **Greedy scheduling** | `build_plan()` | Iterates sorted tasks and fits each one into the time budget. Skipped tasks are stored in `self._skipped` with a reason. Elapsed time is derived from `current_minutes - start_minutes` — no separate counter needed. |
| **Plan explanation** | `explain_plan()` | Returns a plain-English reason for every scheduled and skipped task. Displayed as a collapsible expander in the UI. |
| **Progress tracking** | `progress_report()`, `filter_by_status()` | Tracks done vs remaining tasks per pet. Feeds `st.metric` tiles and the `st.progress` budget bar in the Streamlit UI. |
| **Input validation** | `Task.__post_init__()` | Rejects invalid priority/recurrence values and non-positive durations at object creation time, before any scheduling runs. |

## 📸 Demo Walkthrough

### Streamlit UI (`streamlit run app.py`)

The app has four numbered sections that guide the user from setup to schedule:

**Section 1 — Owner Info**
Enter your name, total daily time budget (in minutes), and preferred start time (`HH:MM`). Click **Save owner**. A green success banner confirms the owner is saved. The owner info bar persists at the top of every section below — Streamlit's `session_state` keeps it alive across interactions.

**Section 2 — Add a Pet**
Enter a pet name, species, breed, and age, then click **Add pet**. The pet is registered with the owner and a `Scheduler` is created for it immediately. Registered pets are listed inline. You can add multiple pets — each gets its own scheduler.

**Section 3 — Add Tasks**
Select which pet the task belongs to, then fill in a title, duration, priority (`high / medium / low`), and recurrence (`daily / weekly / as_needed`). Click **Add task**. Each pet's current task library is visible in a collapsible expander. Adding a task marks any existing plan as stale.

**Section 4 — Today's Schedule**
Click **🗓️ Build Today's Schedule**. The scheduler runs `build_plan()` for every pet and displays:
- A schedule table sorted chronologically via `sort_by_time()`, with priority colour-coded (🔴 high, 🟡 medium, 🟢 low)
- A `st.progress` bar showing time used vs total budget
- A skipped-tasks expander listing anything that didn't fit
- Two `st.metric` tiles — "Tasks to do" and "Completed" — from `filter_by_status()`
- A **"Why was this plan chosen?"** expander with `explain_plan()` output
- If two tasks overlap, a `st.warning` banner appears above the table with a **"Show conflicts"** expander for details
- If two pets' plans overlap (Jordan can't do two things at once), a cross-pet warning banner appears at the top of the section

### Example workflow

```
1. Enter name: Jordan | Budget: 120 min | Start: 08:00 → Save owner
2. Add pet: Biscuit (dog, Golden Retriever, age 3) → Add pet
3. Add tasks to Biscuit:
     Morning walk   30 min  high    daily
     Feeding        10 min  high    daily
     Medication      5 min  high    daily
     Teeth brushing 10 min  medium  daily
     Bath           40 min  low     weekly
4. Click: Build Today's Schedule
5. View sorted table, time budget bar, and explanation panel
6. Expand "Why was this plan chosen?" to read per-task reasoning
```

### Key scheduler behaviors shown in the UI

| Behavior | Where you see it |
|---|---|
| Priority sort | High tasks always appear first in the schedule table |
| Chronological sort | Table rows are in `HH:MM` order via `sort_by_time()` |
| Time budget | Progress bar fills proportionally; skipped tasks listed separately |
| Conflict warning | `st.warning` banner + expandable detail if tasks overlap |
| Plan reasoning | Collapsible `explain_plan()` panel per pet |
| Progress tracking | "Tasks to do" / "Completed" metric tiles |

### CLI output (`python main.py`)

```
════════════════════════════════════════════════════════════
               🐾  PawPal+ — Today's Schedule
════════════════════════════════════════════════════════════
  📅  Wednesday, June 24 2026

  Owner:  Jordan
  Budget: 120 min  │  Start: 08:00
════════════════════════════════════════════════════════════

🐕 Biscuit (Golden Retriever)
────────────────────────────────────────────────────────────
╭─────────────┬──────────────────┬────────────┬────────────┬──────────────╮
│ Time        │ Task             │   Duration │ Priority   │ Recurrence   │
├─────────────┼──────────────────┼────────────┼────────────┼──────────────┤
│ 08:00–08:05 │ 💊 Medication     │      5 min │ ● HIGH     │ 📅 daily      │
│ 08:05–08:15 │ 🍽 Feeding        │     10 min │ ● HIGH     │ 📅 daily      │
│ 08:15–08:45 │ 🚶 Morning walk   │     30 min │ ● HIGH     │ 📅 daily      │
│ 08:45–08:55 │ 🛁 Teeth brushing │     10 min │ ● MED      │ 📅 daily      │
│ 08:55–09:10 │ 🎾 Enrichment toy │     15 min │ ● MED      │ 📅 daily      │
│ 09:10–09:50 │ 🛁 Bath           │     40 min │ ● LOW      │ 📆 weekly     │
╰─────────────┴──────────────────┴────────────┴────────────┴──────────────╯

  Time used: [███████████████████████████░░░] 110/120 min

  Progress: 0/6 tasks complete (0%)
  Still to do:
    ○  💊 Medication  @ 08:00
    ○  🍽 Feeding  @ 08:05
    ○  🚶 Morning walk  @ 08:15
    ○  🛁 Teeth brushing  @ 08:45
    ○  🎾 Enrichment toy  @ 08:55
    ○  🛁 Bath  @ 09:10

🐈 Mochi (Siamese)
────────────────────────────────────────────────────────────
╭─────────────┬────────────────┬────────────┬────────────┬──────────────╮
│ Time        │ Task           │   Duration │ Priority   │ Recurrence   │
├─────────────┼────────────────┼────────────┼────────────┼──────────────┤
│ 08:00–08:05 │ 🧹 Litter box   │      5 min │ ● HIGH     │ 📅 daily      │
│ 08:05–08:15 │ 🍽 Feeding      │     10 min │ ● HIGH     │ 📅 daily      │
│ 08:15–08:25 │ 🛁 Brush coat   │     10 min │ ● MED      │ 📆 weekly     │
│ 08:25–08:40 │ 🎾 Playtime     │     15 min │ ● MED      │ 📅 daily      │
│ 08:40–09:10 │ 🏥 Vet check-up │     30 min │ ● LOW      │ 🔔 as needed  │
╰─────────────┴────────────────┴────────────┴────────────┴──────────────╯

  Time used: [█████████████████░░░░░░░░░░░░░] 70/120 min

  Progress: 0/5 tasks complete (0%)
  Still to do:
    ○  🧹 Litter box  @ 08:00
    ○  🍽 Feeding  @ 08:05
    ○  🛁 Brush coat  @ 08:15
    ○  🎾 Playtime  @ 08:25
    ○  🏥 Vet check-up  @ 08:40

⚠️  Conflict Check
────────────────────────────────────────────────────────────
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Medication' (08:00–08:05) overlaps Mochi·'Litter box' (08:00–08:05)
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Feeding' (08:05–08:15) overlaps Mochi·'Feeding' (08:05–08:15)
  ⚠️  CROSS-PET CONFLICT: Biscuit·'Morning walk' (08:15–08:45) overlaps Mochi·'Brush coat' (08:15–08:25)

💡 Why was this plan chosen?
────────────────────────────────────────────────────────────
Plan explanation for Biscuit (Jordan, 120 min available):

  ✓ Medication: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Morning walk: scheduled first — highest priority
  ✓ Teeth brushing: included — fits within remaining time (priority: medium)
  ✓ Enrichment toy: included — fits within remaining time (priority: medium)
  ✓ Bath: included — fits within remaining time (priority: low)

Plan explanation for Mochi (Jordan, 120 min available):

  ✓ Litter box: scheduled first — highest priority
  ✓ Feeding: scheduled first — highest priority
  ✓ Brush coat: included — fits within remaining time (priority: medium)
  ✓ Playtime: included — fits within remaining time (priority: medium)
  ✓ Vet check-up: included — fits within remaining time (priority: low)

════════════════════════════════════════════════════════════
  All schedules generated.  11 tasks · 180 min planned  🐶🐱
════════════════════════════════════════════════════════════
```

## 🎨 Formatting Features

### CLI (`main.py`)

| Feature | Implementation | Where you see it |
|---|---|---|
| **Structured tables** | `tabulate` library, `rounded_outline` style | Schedule printed as a box-drawn table with aligned columns |
| **ANSI colour-coded priority** | `\033[91m` red / `\033[93m` yellow / `\033[92m` green + `\033[0m` reset | `● HIGH` in red, `● MED` in yellow, `● LOW` in green in the Priority column |
| **Task-type emoji icons** | `task_icon()` keyword matcher in `main.py` | 🚶 walks, 🍽 feeding, 💊 medication, 🛁 grooming, 🎾 enrichment, 🏥 vet, 🧹 litter |
| **Recurrence badges** | `recurrence_badge()` in `main.py` | 📅 daily, 📆 weekly, 🔔 as needed |
| **ASCII progress bar** | Inline string — `█` filled, `░` empty, coloured by % used | `[███████████░░░░░]  110/120 min` — yellow if >85%, red if over budget |
| **Section headers** | `print_section()` with ANSI bold + cyan + dim divider | Cyan bold labels between each output block |
| **Conflict warnings** | Red ANSI on `⚠️ CONFLICT` lines | Conflict lines printed in red; clean result printed in green |

### Streamlit UI (`app.py`)

| Feature | Component | Where you see it |
|---|---|---|
| **Priority colour dots** | `PRIORITY_EMOJI` dict — 🔴 🟡 🟢 | Priority column in every schedule table |
| **Time budget bar** | `st.progress(pct, text=...)` | Fills proportionally; label shows `used / total min` |
| **Conflict banners** | `st.warning(...)` + `st.expander(...)` | Yellow banner above the table; expandable detail list |
| **Progress tiles** | `st.metric("Tasks to do", n)` | Two side-by-side metric cards below each schedule |
| **Skipped tasks** | `st.expander("⏭ Skipped tasks...")` | Collapsible block listing tasks that didn't fit |
| **Reasoning panel** | `st.expander("💡 Why was this plan chosen?")` | Collapsible `explain_plan()` output per pet |

### Libraries used

```bash
pip install tabulate   # CLI table formatting
# streamlit            # already in requirements.txt
```

`tabulate` is a lightweight library with no dependencies. Pass a list of rows, a headers list, and a `tablefmt` string — `"rounded_outline"` gives the box-drawn borders. ANSI colours are built into Python's string literals and need no extra library.

## 🧪 Testing PawPal+

```bash
# Run the full test suite
python -m pytest

# Run with verbose output (shows each test name)
python -m pytest -v

# Run with coverage report
python -m pytest --cov
```

### What the tests cover

The suite has 11 tests split into happy paths and edge cases:

**Happy paths** — normal usage that must always work:
- `test_mark_complete_changes_status` — `Task.mark_complete()` flips `completed` from `False` to `True`
- `test_add_task_increases_pet_task_count` — `Pet.add_task()` correctly grows the task list
- `test_build_plan_orders_high_priority_first` — tasks added out of order are sorted by priority before scheduling

**Sorting correctness:**
- `test_sort_by_time_returns_chronological_order` — `sort_by_time()` returns the built plan in `HH:MM` order regardless of insertion order

**Recurrence logic:**
- `test_daily_task_creates_next_occurrence_tomorrow` — completing a `daily` task creates a new one with `due_date = today + 1 day`
- `test_weekly_task_creates_next_occurrence_in_seven_days` — completing a `weekly` task creates a new one with `due_date = today + 7 days`
- `test_as_needed_task_returns_no_next_occurrence` — completing an `as_needed` task returns `None`

**Conflict detection:**
- `test_check_conflicts_detects_overlapping_tasks` — two tasks manually set to `08:00` trigger a `CONFLICT` warning
- `test_check_conflicts_returns_clean_on_sequential_plan` — a normally built plan produces no conflict warnings

**Edge cases:**
- `test_build_plan_with_no_tasks_returns_empty` — a pet with no tasks returns `[]` without crashing
- `test_task_exceeding_budget_is_skipped` — a 90-min task with a 60-min budget lands in `_skipped`; smaller tasks still schedule

### Test run output

```
====================================================================== test session starts =======================================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\anuja\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 11 items

tests\test_pawpal.py ...........                                                                                                                            [100%]

======================================================================= 11 passed in 0.27s =======================================================================
```

### Confidence Level

⭐⭐⭐⭐⭐ 5 / 5

All 11 automated tests pass, covering sorting, recurrence, conflict detection, empty plans, and budget overflow. Every core scheduling behavior has at least one happy-path test and one edge-case test.