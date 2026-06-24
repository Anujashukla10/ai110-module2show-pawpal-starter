"""
PawPal+ — class skeletons (v2)
Changes from v1:
  - Task.reset() clears stale scheduled_time / completed
  - build_plan() deep-copies tasks before mutating, guards empty list
  - check_conflicts() raises RuntimeError if called before build_plan()
  - Owner gets a pets list; Scheduler validates ownership on init
  - Scheduler.add_task() wires UI → pet cleanly
  - display_schedule() handles empty plan gracefully
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import copy


# ─────────────────────────────────────────────
# Task
# ─────────────────────────────────────────────

@dataclass
class Task:
    """Represents a single pet care task."""

    title: str
    duration_minutes: int
    priority: str                          # "high" | "medium" | "low"
    recurrence: str = "daily"             # "daily" | "weekly" | "as_needed"
    scheduled_time: Optional[str] = None  # assigned by Scheduler
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if priority is 'high'."""
        return self.priority == "high"

    def priority_score(self) -> int:
        """Convert priority label to a numeric score for sorting.

        Returns:
            3 for 'high', 2 for 'medium', 1 for 'low', 0 for unknown.
        """
        return {"high": 3, "medium": 2, "low": 1}.get(self.priority, 0)

    def reset(self) -> None:
        """Clear scheduled_time and completed so the task can be rescheduled.

        Call this (or rely on build_plan's deep-copy) before re-running
        the scheduler so stale state from a previous run doesn't leak.
        """
        self.scheduled_time = None
        self.completed = False

    def __repr__(self) -> str:
        time = self.scheduled_time or "unscheduled"
        return (
            f"Task({self.title!r}, {self.duration_minutes}min, "
            f"priority={self.priority!r}, time={time!r})"
        )


# ─────────────────────────────────────────────
# Pet
# ─────────────────────────────────────────────

@dataclass
class Pet:
    """Represents the owner's pet."""

    name: str
    species: str          # e.g. "dog", "cat", "other"
    breed: str = ""
    age: int = 0
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet's task list."""
        self._tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of the task list."""
        return list(self._tasks)

    def remove_task(self, title: str) -> None:
        """Remove a task by title (case-insensitive). Raises ValueError if not found."""
        for task in self._tasks:
            if task.title.lower() == title.lower():
                self._tasks.remove(task)
                return
        raise ValueError(f"No task with title {title!r} found.")

    def __repr__(self) -> str:
        return (
            f"Pet(name={self.name!r}, species={self.species!r}, "
            f"tasks={len(self._tasks)})"
        )


# ─────────────────────────────────────────────
# Owner
# ─────────────────────────────────────────────

@dataclass
class Owner:
    """Represents the pet owner and their scheduling constraints."""

    name: str
    available_minutes: int = 120
    preferred_start: str = "08:00"
    preferences: dict = field(default_factory=dict)
    # FIX: Owner now holds its own pets so the Owner→Pet relationship
    # from the UML is enforced in code, not just in the diagram.
    pets: list[Pet] = field(default_factory=list, repr=False)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def set_availability(self, minutes: int) -> None:
        """Update the daily time budget."""
        self.available_minutes = minutes

    def add_preference(self, key: str, value) -> None:
        """Store an owner preference (e.g. add_preference('rest_day', 'Monday'))."""
        self.preferences[key] = value

    def get_preferences(self) -> dict:
        """Return the full preferences dict."""
        return self.preferences

    def __repr__(self) -> str:
        return (
            f"Owner(name={self.name!r}, "
            f"available_minutes={self.available_minutes}, "
            f"pets={[p.name for p in self.pets]})"
        )


# ─────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────

class Scheduler:
    """Builds and explains a daily care plan for a pet."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        # FIX: validate ownership so mismatched owner/pet combos are caught early.
        if owner.pets and pet not in owner.pets:
            raise ValueError(
                f"{pet.name!r} does not belong to owner {owner.name!r}. "
                "Call owner.add_pet(pet) first."
            )
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.plan: list[Task] = []
        self.start_time: str = owner.preferred_start

    # ── Task management ───────────────────────

    def add_task(self, task: Task) -> None:
        """Add a task directly via Scheduler — clean wire from the Streamlit UI.

        Usage in app.py:
            scheduler.add_task(Task(title, duration, priority))
        This delegates to pet.add_task() so there is exactly one source of truth.
        """
        self.pet.add_task(task)

    # ── Sorting & filtering ───────────────────

    def sort_tasks(self) -> list[Task]:
        """Return tasks sorted by priority_score (desc), then duration (asc)."""
        return sorted(
            self.pet.get_tasks(),
            key=lambda t: (-t.priority_score(), t.duration_minutes),
        )

    def filter_by_priority(self, level: str) -> list[Task]:
        """Return only tasks matching the given priority level."""
        return [t for t in self.pet.get_tasks() if t.priority == level]

    # ── Core scheduling ───────────────────────

    def build_plan(self) -> list[Task]:
        """Assign scheduled_time to each task that fits within the time budget.

        FIX: deep-copies tasks before mutating so pet._tasks is never touched,
        and guards against an empty task list.
        """
        tasks = self.sort_tasks()

        # FIX: guard — return early with a clear empty list, not silent None.
        if not tasks:
            self.plan = []
            return self.plan

        # Parse start time into total minutes since midnight.
        start_h, start_m = map(int, self.start_time.split(":"))
        current_minutes = start_h * 60 + start_m
        elapsed = 0
        scheduled = []

        for task in tasks:
            if elapsed + task.duration_minutes > self.owner.available_minutes:
                continue  # skip — not enough time left

            # FIX: work on a copy so the original Task in pet._tasks is untouched.
            task_copy = copy.copy(task)
            task_copy.reset()

            slot_h, slot_m = divmod(current_minutes, 60)
            task_copy.scheduled_time = f"{slot_h:02d}:{slot_m:02d}"

            current_minutes += task.duration_minutes
            elapsed += task.duration_minutes
            scheduled.append(task_copy)

        self.plan = scheduled
        return self.plan

    def check_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose time slots overlap.

        FIX: raises RuntimeError if build_plan() hasn't been called yet,
        so callers get a clear message instead of a silent empty result.
        """
        if not self.plan:
            raise RuntimeError(
                "No plan found. Call build_plan() before check_conflicts()."
            )

        conflicts = []
        for i, a in enumerate(self.plan):
            for b in self.plan[i + 1:]:
                a_end = self._time_to_minutes(a.scheduled_time) + a.duration_minutes
                b_start = self._time_to_minutes(b.scheduled_time)
                if a_end > b_start:
                    conflicts.append((a, b))
        return conflicts

    # ── Output ────────────────────────────────

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was included."""
        if not self.plan:
            return "No tasks were scheduled. Add tasks or increase available time."

        lines = [f"Plan explanation for {self.pet.name}:\n"]
        for task in self.plan:
            reason = (
                "high priority — scheduled first"
                if task.is_high_priority()
                else f"priority={task.priority!r} — fit within time budget"
            )
            lines.append(f"  • {task.title}: {reason}")
        return "\n".join(lines)

    def display_schedule(self) -> str:
        """Format self.plan as a printable daily schedule string.

        FIX: handles empty plan gracefully with a friendly message.

        Example output:
            Daily plan for Biscuit (dog):
              08:00 — Morning walk (30 min) [priority: high]
              08:30 — Feeding (10 min) [priority: high]
        """
        if not self.plan:
            return (
                f"Daily plan for {self.pet.name} ({self.pet.species}):\n"
                "  No tasks scheduled. Add tasks or increase available time."
            )

        lines = [f"Daily plan for {self.pet.name} ({self.pet.species}):"]
        for task in self.plan:
            lines.append(
                f"  {task.scheduled_time} — {task.title} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )
        return "\n".join(lines)

    # ── Helpers ───────────────────────────────

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert 'HH:MM' string to total minutes since midnight."""
        h, m = map(int, time_str.split(":"))
        return h * 60 + m

    def __repr__(self) -> str:
        return (
            f"Scheduler(owner={self.owner.name!r}, "
            f"pet={self.pet.name!r}, "
            f"tasks_in_plan={len(self.plan)})"
        )