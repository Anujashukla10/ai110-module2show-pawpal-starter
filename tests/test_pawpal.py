"""
PawPal+ — test suite
Run with: python -m pytest -v

Tests are grouped into:
  Happy paths  — normal usage that should always work
  Edge cases   — boundary conditions and unusual inputs
"""

import copy
import datetime
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def owner():
    """A basic owner with a 60-minute budget."""
    return Owner(name="Jordan", available_minutes=60, preferred_start="08:00")


@pytest.fixture
def dog(owner):
    """A registered dog pet."""
    pet = Pet(name="Biscuit", species="dog")
    owner.add_pet(pet)
    return pet


@pytest.fixture
def scheduler(owner, dog):
    """A scheduler wired to the owner and dog."""
    return Scheduler(owner=owner, pet=dog)


# ─────────────────────────────────────────────
# HAPPY PATH 1 — Task completion flips status
# ─────────────────────────────────────────────

def test_mark_complete_changes_status():
    """Task.mark_complete() should flip completed from False to True."""
    task = Task(title="Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ─────────────────────────────────────────────
# HAPPY PATH 2 — Adding a task increases pet count
# ─────────────────────────────────────────────

def test_add_task_increases_pet_task_count():
    """Pet.add_task() should increase the pet's task count by 1."""
    pet = Pet(name="Biscuit", species="dog")

    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.get_tasks()) == 1


# ─────────────────────────────────────────────
# SORTING — tasks returned in chronological order
# ─────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order(scheduler):
    """sort_by_time() must return tasks in HH:MM order regardless of insertion order."""
    # Add tasks in reverse time order on purpose
    scheduler.add_task(Task("Evening meds",  5, "high",   recurrence="daily"))
    scheduler.add_task(Task("Afternoon walk",20, "medium", recurrence="daily"))
    scheduler.add_task(Task("Morning feed",  10, "high",   recurrence="daily"))
    scheduler.build_plan()

    sorted_tasks = scheduler.sort_by_time()
    times = [t.scheduled_time for t in sorted_tasks]

    # Each time should be <= the next one
    assert times == sorted(times), (
        f"Expected chronological order but got: {times}"
    )


def test_build_plan_orders_high_priority_first(scheduler):
    """build_plan() should place high-priority tasks before low-priority ones."""
    # Add low priority first — scheduler must reorder, not preserve insertion order
    scheduler.add_task(Task("Bath",         20, "low",  recurrence="weekly"))
    scheduler.add_task(Task("Morning walk", 30, "high", recurrence="daily"))
    scheduler.build_plan()

    titles = [t.title for t in scheduler.plan]
    assert titles.index("Morning walk") < titles.index("Bath")


# ─────────────────────────────────────────────
# RECURRENCE — daily task creates tomorrow's occurrence
# ─────────────────────────────────────────────

def test_daily_task_creates_next_occurrence_tomorrow(scheduler):
    """mark_task_complete() on a daily task should create a new task due tomorrow."""
    today = datetime.date.today()
    scheduler.add_task(Task("Feeding", 10, "high", recurrence="daily"))
    scheduler.build_plan()

    next_task = scheduler.mark_task_complete("Feeding")

    assert next_task is not None
    assert next_task.due_date == today + datetime.timedelta(days=1)
    assert next_task.completed is False
    assert next_task.title == "Feeding"        # same task, new occurrence
    assert next_task.recurrence == "daily"     # recurrence is preserved


def test_weekly_task_creates_next_occurrence_in_seven_days(scheduler):
    """mark_task_complete() on a weekly task should create a new task due in 7 days."""
    today = datetime.date.today()
    scheduler.add_task(Task("Bath", 20, "medium", recurrence="weekly"))
    scheduler.build_plan()

    next_task = scheduler.mark_task_complete("Bath")

    assert next_task is not None
    assert next_task.due_date == today + datetime.timedelta(weeks=1)
    assert next_task.completed is False


def test_as_needed_task_returns_no_next_occurrence(scheduler):
    """mark_task_complete() on an as_needed task should return None — no auto-recurrence."""
    scheduler.add_task(Task("Vet check-up", 30, "low", recurrence="as_needed"))
    scheduler.build_plan()

    result = scheduler.mark_task_complete("Vet check-up")

    assert result is None


# ─────────────────────────────────────────────
# CONFLICT DETECTION — flags overlapping time slots
# ─────────────────────────────────────────────

def test_check_conflicts_detects_overlapping_tasks(scheduler):
    """check_conflicts() must return at least one warning when two tasks share a time window."""
    task_a = copy.copy(Task("Morning walk", 30, "high"))
    task_a.scheduled_time = "08:00"   # 08:00 – 08:30

    task_b = copy.copy(Task("Feeding", 10, "high"))
    task_b.scheduled_time = "08:00"   # 08:00 – 08:10  ← overlaps task_a

    scheduler.plan = [task_a, task_b]
    warnings = scheduler.check_conflicts()

    assert len(warnings) >= 1
    assert any("CONFLICT" in w for w in warnings)


def test_check_conflicts_returns_clean_on_sequential_plan(scheduler):
    """check_conflicts() must return no warnings when tasks don't overlap."""
    scheduler.add_task(Task("Feeding",      10, "high", recurrence="daily"))
    scheduler.add_task(Task("Morning walk", 30, "high", recurrence="daily"))
    scheduler.build_plan()  # build_plan never produces overlaps

    warnings = scheduler.check_conflicts()

    # Any items returned should be info messages, not conflict warnings
    assert not any("CONFLICT" in w for w in warnings)


# ─────────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────────

def test_build_plan_with_no_tasks_returns_empty(scheduler):
    """build_plan() on a pet with no tasks should return an empty list, not crash."""
    result = scheduler.build_plan()

    assert result == []
    assert scheduler.plan == []


def test_task_exceeding_budget_is_skipped(scheduler):
    """A task longer than available_minutes should be skipped without blocking shorter tasks."""
    # owner has 60 min; Long hike needs 90
    scheduler.add_task(Task("Long hike", 90, "high",   recurrence="daily"))
    scheduler.add_task(Task("Feeding",   10, "medium", recurrence="daily"))
    scheduler.build_plan()

    scheduled_titles = [t.title for t in scheduler.plan]
    skipped_titles   = [t.title for t in scheduler._skipped]

    assert "Long hike" in skipped_titles
    assert "Feeding"   in scheduled_titles