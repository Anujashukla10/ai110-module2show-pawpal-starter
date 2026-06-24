"""
PawPal+ — full implementation (v4)
All methods have 1-line docstrings.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import copy
import datetime


# ─────────────────────────────────────────────
# Task
# ─────────────────────────────────────────────

@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str                              # "high" | "medium" | "low"
    recurrence: str = "daily"                 # "daily" | "weekly" | "as_needed"
    scheduled_time: Optional[str] = None      # "HH:MM", assigned by Scheduler
    completed: bool = False
    due_date: datetime.date = field(          # defaults to today
        default_factory=datetime.date.today
    )

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

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task due on the next recurrence date (daily+1, weekly+7), or None for as_needed."""
        if self.recurrence == "as_needed":
            return None   # no automatic recurrence for one-off tasks

        if self.recurrence == "daily":
            next_date = self.due_date + datetime.timedelta(days=1)
        else:  # "weekly"
            next_date = self.due_date + datetime.timedelta(weeks=1)

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurrence=self.recurrence,
            scheduled_time=None,   # Scheduler will assign this
            completed=False,
            due_date=next_date,
        )

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

    def sort_by_time(self) -> list[Task]:
        """Return self.plan sorted chronologically using 'HH:MM' string comparison as a proxy for time order."""
        if not self.plan:
            raise RuntimeError(
                "No plan built yet — call build_plan() before sort_by_time()."
            )
        return sorted(
            self.plan,
            key=lambda t: t.scheduled_time or "99:99"
        )

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return planned tasks where completed matches the given bool (True=done, False=to-do)."""
        if not self.plan:
            raise RuntimeError(
                "No plan built yet — call build_plan() before filter_by_status()."
            )
        return [t for t in self.plan if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return this scheduler's plan if the pet name matches, or an empty list if it doesn't."""
        if self.pet.name.lower() != pet_name.lower():
            return []
        return list(self.plan)

    def build_plan(self) -> list[Task]:
        """Greedily fit sorted tasks into the owner's time budget and store in self.plan."""
        tasks = self.sort_tasks()
        self._skipped = []

        if not tasks:
            self.plan = []
            return self.plan

        start_h, start_m = map(int, self.start_time.split(":"))
        start_minutes   = start_h * 60 + start_m
        current_minutes = start_minutes   # moves forward as tasks are added
        scheduled = []

        for task in tasks:
            # elapsed is derived — no need to track it as a separate variable
            elapsed = current_minutes - start_minutes
            if elapsed + task.duration_minutes > self.owner.available_minutes:
                self._skipped.append(task)
                continue

            task_copy = copy.copy(task)
            task_copy.reset()
            slot_h, slot_m = divmod(current_minutes, 60)
            task_copy.scheduled_time = f"{slot_h:02d}:{slot_m:02d}"

            current_minutes += task.duration_minutes
            scheduled.append(task_copy)

        self.plan = scheduled
        return self.plan

    def check_conflicts(self) -> list[str]:
        """Return human-readable warning strings for every overlapping time window in self.plan; never raises."""
        if not self.plan:
            return ["ℹ️  No plan built yet — call build_plan() first."]

        warnings = []
        for i, a in enumerate(self.plan):
            for b in self.plan[i + 1:]:
                a_start = self._to_minutes(a.scheduled_time)
                a_end   = a_start + a.duration_minutes
                b_start = self._to_minutes(b.scheduled_time)
                b_end   = b_start + b.duration_minutes

                # Overlap condition: a starts before b ends AND b starts before a ends
                if a_start < b_end and b_start < a_end:
                    a_end_str = self._minutes_to_time(a_end)
                    b_end_str = self._minutes_to_time(b_end)
                    warnings.append(
                        f"⚠️  CONFLICT on {self.pet.name}: "
                        f"'{a.title}' ({a.scheduled_time}–{a_end_str}) "
                        f"overlaps '{b.title}' ({b.scheduled_time}–{b_end_str})"
                    )
        return warnings

    @staticmethod
    def check_cross_pet_conflicts(schedulers: list["Scheduler"]) -> list[str]:
        """Return warning strings for time-window overlaps across different pets' plans; never raises."""
        # Flatten all plans into (pet_name, task) tuples
        all_tasks: list[tuple[str, Task]] = []
        for sched in schedulers:
            for task in sched.plan:
                all_tasks.append((sched.pet.name, task))

        if not all_tasks:
            return ["ℹ️  No plans found — call build_plan() on each scheduler first."]

        warnings = []
        for i, (pet_a, a) in enumerate(all_tasks):
            for pet_b, b in all_tasks[i + 1:]:
                if pet_a == pet_b:
                    continue   # same-pet conflicts handled by check_conflicts()

                a_start = Scheduler._to_minutes(a.scheduled_time)
                a_end   = a_start + a.duration_minutes
                b_start = Scheduler._to_minutes(b.scheduled_time)
                b_end   = b_start + b.duration_minutes

                if a_start < b_end and b_start < a_end:
                    a_end_str = Scheduler._minutes_to_time(a_end)
                    b_end_str = Scheduler._minutes_to_time(b_end)
                    warnings.append(
                        f"⚠️  CROSS-PET CONFLICT: "
                        f"{pet_a}·'{a.title}' ({a.scheduled_time}–{a_end_str}) "
                        f"overlaps "
                        f"{pet_b}·'{b.title}' ({b.scheduled_time}–{b_end_str})"
                    )
        return warnings

    def mark_task_complete(self, title: str) -> Optional[Task]:
        """Mark a planned task done by title, auto-register its next occurrence, and return it (or None)."""
        for task in self.plan:
            if task.title.lower() == title.lower():
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    # Remove the stale original from pet._tasks and add the
                    # next occurrence so the pet's library stays current.
                    try:
                        self.pet.remove_task(task.title)
                    except ValueError:
                        pass  # already removed or was a copy — safe to skip
                    self.pet.add_task(next_task)
                return next_task
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

    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """Convert total minutes since midnight back to an 'HH:MM' string."""
        h, m = divmod(minutes, 60)
        return f"{h:02d}:{m:02d}"

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