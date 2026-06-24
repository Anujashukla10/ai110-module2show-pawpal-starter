"""
PawPal+ — full implementation (v4)
All methods have 1-line docstrings.
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
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str                          # "high" | "medium" | "low"
    recurrence: str = "daily"             # "daily" | "weekly" | "as_needed"
    scheduled_time: Optional[str] = None  # "HH:MM", assigned by Scheduler
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate priority, recurrence, and duration on creation."""
        valid_priorities = {"high", "medium", "low"}
        valid_recurrences = {"daily", "weekly", "as_needed"}
        if self.priority not in valid_priorities:
            raise ValueError(
                f"priority must be one of {valid_priorities}, got {self.priority!r}"
            )
        if self.recurrence not in valid_recurrences:
            raise ValueError(
                f"recurrence must be one of {valid_recurrences}, got {self.recurrence!r}"
            )
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be a positive integer.")

    def mark_complete(self) -> None:
        """Set completed to True to record this task as done."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"

    def priority_score(self) -> int:
        """Return 3 for high, 2 for medium, or 1 for low priority."""
        return {"high": 3, "medium": 2, "low": 1}[self.priority]

    def reset(self) -> None:
        """Clear scheduled_time and completed so the task can be rescheduled."""
        self.scheduled_time = None
        self.completed = False

    def summary(self) -> str:
        """Return a one-line human-readable description of this task."""
        time = self.scheduled_time or "unscheduled"
        status = "✓" if self.completed else "○"
        return (
            f"{status} [{self.priority.upper()}] {self.title} "
            f"({self.duration_minutes} min) @ {time} — {self.recurrence}"
        )

    def __repr__(self) -> str:
        """Return a concise developer-facing string for this task."""
        return (
            f"Task({self.title!r}, {self.duration_minutes}min, "
            f"priority={self.priority!r}, time={self.scheduled_time!r})"
        )


# ─────────────────────────────────────────────
# Pet
# ─────────────────────────────────────────────

@dataclass
class Pet:
    """Stores pet details and owns a list of care tasks."""

    name: str
    species: str
    breed: str = ""
    age: int = 0
    _tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's list, rejecting duplicate titles."""
        titles = [t.title.lower() for t in self._tasks]
        if task.title.lower() in titles:
            raise ValueError(
                f"Task {task.title!r} already exists for {self.name}. "
                "Use remove_task() first if you want to replace it."
            )
        self._tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self._tasks)

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        """Return only the tasks that match the given priority level."""
        return [t for t in self._tasks if t.priority == priority]

    def remove_task(self, title: str) -> None:
        """Remove a task by title (case-insensitive), raising ValueError if missing."""
        for task in self._tasks:
            if task.title.lower() == title.lower():
                self._tasks.remove(task)
                return
        raise ValueError(f"No task named {title!r} found for {self.name}.")

    def clear_tasks(self) -> None:
        """Delete all tasks from this pet's list."""
        self._tasks.clear()

    def total_task_minutes(self) -> int:
        """Return the total duration in minutes across all tasks."""
        return sum(t.duration_minutes for t in self._tasks)

    def summary(self) -> str:
        """Return a multi-line overview of this pet and all its tasks."""
        lines = [f"🐾 {self.name} ({self.species}"
                 + (f", {self.breed}" if self.breed else "")
                 + (f", age {self.age}" if self.age else "") + ")"]
        if self._tasks:
            for task in self._tasks:
                lines.append(f"   {task.summary()}")
        else:
            lines.append("   No tasks yet.")
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return a concise developer-facing string for this pet."""
        return (
            f"Pet(name={self.name!r}, species={self.species!r}, "
            f"tasks={len(self._tasks)})"
        )


# ─────────────────────────────────────────────
# Owner
# ─────────────────────────────────────────────

@dataclass
class Owner:
    """Manages multiple pets and the owner's daily scheduling constraints."""

    name: str
    available_minutes: int = 120
    preferred_start: str = "08:00"
    preferences: dict = field(default_factory=dict)
    _pets: list[Pet] = field(default_factory=list, repr=False)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner, rejecting duplicate names."""
        names = [p.name.lower() for p in self._pets]
        if pet.name.lower() in names:
            raise ValueError(f"A pet named {pet.name!r} is already registered.")
        self._pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return a list of all pets registered to this owner."""
        return list(self._pets)

    def get_pet(self, name: str) -> Pet:
        """Look up and return a pet by name, raising ValueError if not found."""
        for pet in self._pets:
            if pet.name.lower() == name.lower():
                return pet
        raise ValueError(f"No pet named {name!r} found for owner {self.name!r}.")

    def remove_pet(self, name: str) -> None:
        """Unregister a pet by name, raising ValueError if not found."""
        pet = self.get_pet(name)
        self._pets.remove(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task across all registered pets."""
        return [(pet, task) for pet in self._pets for task in pet.get_tasks()]

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks belonging to the named pet."""
        return self.get_pet(pet_name).get_tasks()

    def set_availability(self, minutes: int) -> None:
        """Update the owner's daily time budget in minutes."""
        if minutes <= 0:
            raise ValueError("available_minutes must be positive.")
        self.available_minutes = minutes

    def add_preference(self, key: str, value) -> None:
        """Store a key-value scheduling preference for this owner."""
        self.preferences[key] = value

    def get_preferences(self) -> dict:
        """Return the full dictionary of owner preferences."""
        return self.preferences

    def summary(self) -> str:
        """Return a multi-line overview of the owner, budget, and all pets."""
        lines = [
            f"👤 {self.name}  |  {self.available_minutes} min/day  "
            f"|  starts {self.preferred_start}"
        ]
        if self._pets:
            for pet in self._pets:
                lines.append(pet.summary())
        else:
            lines.append("  No pets registered yet.")
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return a concise developer-facing string for this owner."""
        return (
            f"Owner(name={self.name!r}, "
            f"available_minutes={self.available_minutes}, "
            f"pets={[p.name for p in self._pets]})"
        )


# ─────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────

class Scheduler:
    """Retrieves tasks from Owner → Pet, organises, and schedules them."""

    def __init__(self, owner: Owner, pet: Pet) -> None:
        """Initialise with an owner and one of their pets, validating ownership."""
        if owner.get_pets() and pet not in owner.get_pets():
            raise ValueError(
                f"{pet.name!r} is not registered with owner {owner.name!r}. "
                "Call owner.add_pet(pet) first."
            )
        self.owner: Owner = owner
        self.pet: Pet = pet
        self.plan: list[Task] = []
        self.start_time: str = owner.preferred_start
        self._skipped: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task via Scheduler, delegating to pet.add_task() as the single source of truth."""
        self.pet.add_task(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by title, delegating to pet.remove_task()."""
        self.pet.remove_task(title)

    def sort_tasks(self) -> list[Task]:
        """Retrieve tasks from Owner and sort by priority descending, then duration ascending."""
        tasks = self.owner.get_tasks_for_pet(self.pet.name)
        return sorted(tasks, key=lambda t: (-t.priority_score(), t.duration_minutes))

    def filter_by_priority(self, level: str) -> list[Task]:
        """Return only the tasks that match the given priority level."""
        return [t for t in self.owner.get_tasks_for_pet(self.pet.name)
                if t.priority == level]

    def filter_by_recurrence(self, recurrence: str) -> list[Task]:
        """Return only the tasks that match the given recurrence pattern."""
        return [t for t in self.owner.get_tasks_for_pet(self.pet.name)
                if t.recurrence == recurrence]

    def build_plan(self) -> list[Task]:
        """Greedily fit sorted tasks into the owner's time budget and store in self.plan."""
        tasks = self.sort_tasks()
        self._skipped = []

        if not tasks:
            self.plan = []
            return self.plan

        start_h, start_m = map(int, self.start_time.split(":"))
        current_minutes = start_h * 60 + start_m
        elapsed = 0
        scheduled = []

        for task in tasks:
            if elapsed + task.duration_minutes > self.owner.available_minutes:
                self._skipped.append(task)
                continue

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
        """Return overlapping (task_a, task_b) pairs, raising RuntimeError if build_plan() hasn't run."""
        if not self.plan:
            raise RuntimeError(
                "self.plan is empty — call build_plan() before check_conflicts()."
            )
        conflicts = []
        for i, a in enumerate(self.plan):
            for b in self.plan[i + 1:]:
                a_end = self._to_minutes(a.scheduled_time) + a.duration_minutes
                b_start = self._to_minutes(b.scheduled_time)
                if a_end > b_start:
                    conflicts.append((a, b))
        return conflicts

    def mark_task_complete(self, title: str) -> None:
        """Mark a scheduled task as complete by title, raising ValueError if not found."""
        for task in self.plan:
            if task.title.lower() == title.lower():
                task.mark_complete()
                return
        raise ValueError(f"No scheduled task named {title!r}. Run build_plan() first.")

    def display_schedule(self) -> str:
        """Return a formatted daily schedule string ready for the terminal or Streamlit."""
        header = (
            f"Daily plan for {self.pet.name} ({self.pet.species})  "
            f"[budget: {self.owner.available_minutes} min, "
            f"start: {self.start_time}]"
        )
        if not self.plan:
            return header + "\n  No tasks scheduled. Add tasks or increase budget."

        lines = [header]
        for task in self.plan:
            lines.append(
                f"  {task.scheduled_time} — {task.title} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )

        used = sum(t.duration_minutes for t in self.plan)
        lines.append(f"\n  Time used: {used} / {self.owner.available_minutes} min")

        if self._skipped:
            lines.append("  Skipped (not enough time):")
            for t in self._skipped:
                lines.append(f"    • {t.title} ({t.duration_minutes} min)")

        return "\n".join(lines)

    def explain_plan(self) -> str:
        """Return a plain-English explanation of why each task was included or skipped."""
        if not self.plan:
            return (
                f"No plan built for {self.pet.name} yet. "
                "Call build_plan() to generate one."
            )

        lines = [f"Plan explanation for {self.pet.name} "
                 f"({self.owner.name}, {self.owner.available_minutes} min available):\n"]

        for task in self.plan:
            reason = (
                "scheduled first — highest priority"
                if task.is_high_priority()
                else f"included — fits within remaining time (priority: {task.priority})"
            )
            lines.append(f"  ✓ {task.title}: {reason}")

        for task in self._skipped:
            lines.append(
                f"  ✗ {task.title}: skipped — "
                f"{task.duration_minutes} min needed but budget exhausted"
            )

        return "\n".join(lines)

    def progress_report(self) -> str:
        """Return a completion summary showing done vs remaining tasks."""
        if not self.plan:
            return "No plan built yet."
        done = [t for t in self.plan if t.completed]
        remaining = [t for t in self.plan if not t.completed]
        lines = [
            f"Progress for {self.pet.name}: "
            f"{len(done)}/{len(self.plan)} tasks complete"
        ]
        if remaining:
            lines.append("  Still to do:")
            for t in remaining:
                lines.append(f"    • {t.title} @ {t.scheduled_time}")
        return "\n".join(lines)

    @staticmethod
    def _to_minutes(time_str: str) -> int:
        """Convert an 'HH:MM' string to total minutes since midnight."""
        h, m = map(int, time_str.split(":"))
        return h * 60 + m

    def __repr__(self) -> str:
        """Return a concise developer-facing string for this scheduler."""
        return (
            f"Scheduler(owner={self.owner.name!r}, "
            f"pet={self.pet.name!r}, "
            f"tasks_in_plan={len(self.plan)})"
        )


# ─────────────────────────────────────────────
# Quick smoke-test  (python pawpal_system.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    owner = Owner(name="Jordan", available_minutes=90, preferred_start="08:00")
    dog   = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    owner.add_pet(dog)

    scheduler = Scheduler(owner=owner, pet=dog)
    scheduler.add_task(Task("Morning walk",   30, "high",   recurrence="daily"))
    scheduler.add_task(Task("Feeding",        10, "high",   recurrence="daily"))
    scheduler.add_task(Task("Medication",      5, "high",   recurrence="daily"))
    scheduler.add_task(Task("Teeth brushing", 10, "medium", recurrence="daily"))
    scheduler.add_task(Task("Enrichment",     20, "medium", recurrence="daily"))
    scheduler.add_task(Task("Bath",           40, "low",    recurrence="weekly"))

    scheduler.build_plan()
    print(scheduler.display_schedule())
    print()
    print(scheduler.explain_plan())
    print()

    scheduler.mark_task_complete("Morning walk")
    print(scheduler.progress_report())