"""
PawPal+ — class skeletons
Generated from UML class diagram.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


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
    scheduled_time: Optional[str] = None  # e.g. "08:00", assigned by Scheduler
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def is_high_priority(self) -> bool:
        """Return True if priority is 'high'."""
        pass

    def priority_score(self) -> int:
        """Convert priority label to a numeric score for sorting.

        Returns:
            3 for 'high', 2 for 'medium', 1 for 'low'.
        """
        pass

    def __repr__(self) -> str:
        pass


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
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove a task by title. Raises ValueError if not found."""
        pass

    def __repr__(self) -> str:
        pass


# ─────────────────────────────────────────────
# Owner
# ─────────────────────────────────────────────

@dataclass
class Owner:
    """Represents the pet owner and their scheduling constraints."""

    name: str
    available_minutes: int = 120          # total time budget for the day
    preferred_start: str = "08:00"        # e.g. "08:00"
    preferences: dict = field(default_factory=dict)

    def set_availability(self, minutes: int) -> None:
        """Update the daily time budget."""
        pass

    def add_preference(self, key: str, value) -> None:
        """Store an owner preference (e.g. 'skip_grooming_on': 'Monday')."""
        pass

    def get_preferences(self) -> dict:
        """Return the full preferences dict."""
        pass

    def __repr__(self) -> str:
        pass


# ─────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────

class Scheduler:
    """Builds and explains a daily care plan for a pet."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.plan: list[Task] = []
        self.start_time: str = owner.preferred_start

    def sort_tasks(self) -> list[Task]:
        """Return tasks sorted by priority_score (desc), then duration (asc)."""
        pass

    def filter_by_priority(self, level: str) -> list[Task]:
        """Return only tasks matching the given priority level."""
        pass

    def build_plan(self) -> list[Task]:
        """Assign scheduled_time to each task that fits within the time budget.

        Algorithm sketch:
            1. sort_tasks()
            2. Walk sorted list; track elapsed minutes.
            3. Add task to plan if elapsed + duration <= available_minutes.
            4. Store result in self.plan and return it.
        """
        pass

    def check_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose time slots overlap."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was included."""
        pass

    def display_schedule(self) -> str:
        """Format self.plan as a printable daily schedule string.

        Example output:
            Daily plan for Biscuit (dog):
              08:00 — Morning walk (30 min) [priority: high]
              08:30 — Feeding (10 min) [priority: high]
        """
        pass

    def __repr__(self) -> str:
        return (
            f"Scheduler(owner={self.owner.name!r}, "
            f"pet={self.pet.name!r}, "
            f"tasks_in_plan={len(self.plan)})"
        )