"""
PawPal+ — main.py (v5)
Demos lightweight conflict detection:
  - Same-pet conflict:  two tasks manually forced to the same time slot
  - Cross-pet conflict: dog and cat tasks overlapping on Jordan's schedule
"""

import copy
import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


def print_warnings(warnings: list[str], label: str) -> None:
    """Print a labelled block of conflict warnings (or a clean bill of health)."""
    thin = "-" * 54
    print(f"\n{thin}")
    print(f"  {label}")
    print(thin)
    if warnings:
        for w in warnings:
            print(f"  {w}")
    else:
        print("  ✅  No conflicts detected.")


def main():
    divider = "=" * 54
    today   = datetime.date.today()

    print(divider)
    print("   🐾  PawPal+ — Conflict Detection Demo  🐾")
    print(divider)
    print(f"   Today: {today.strftime('%A, %B %d %Y')}")
    print(divider)

    # ── Setup ─────────────────────────────────────────────────────────
    owner = Owner(name="Jordan", available_minutes=120, preferred_start="08:00")
    dog   = Pet(name="Biscuit", species="dog")
    cat   = Pet(name="Mochi",   species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # ── SCENARIO 1: Normal plan — no conflicts ─────────────────────────
    print("\n── SCENARIO 1: Normal plan (expect no conflicts) ──\n")

    dog_sched = Scheduler(owner=owner, pet=dog)
    dog_sched.add_task(Task("Morning walk", 30, "high",   recurrence="daily"))
    dog_sched.add_task(Task("Feeding",      10, "high",   recurrence="daily"))
    dog_sched.add_task(Task("Medication",    5, "high",   recurrence="daily"))
    dog_sched.build_plan()

    for t in dog_sched.sort_by_time():
        print(f"   {t.scheduled_time} — {t.title} ({t.duration_minutes} min)")

    print_warnings(dog_sched.check_conflicts(), "Same-pet conflict check — Biscuit")

    # ── SCENARIO 2: Force a same-pet conflict ─────────────────────────
    # build_plan() schedules tasks sequentially so they never overlap.
    # To test detection we manually set two tasks to the same start time,
    # simulating a bug or a manually overridden schedule.
    print("\n\n── SCENARIO 2: Same-pet conflict (forced overlap) ──\n")
    print("   Manually setting 'Feeding' and 'Morning walk' to 08:00...")

    conflict_dog = Scheduler(owner=owner, pet=dog)

    # Bypass build_plan and inject tasks with clashing times directly
    task_a = copy.copy(Task("Morning walk", 30, "high"))
    task_a.scheduled_time = "08:00"   # 08:00 – 08:30

    task_b = copy.copy(Task("Feeding", 10, "high"))
    task_b.scheduled_time = "08:00"   # 08:00 – 08:10  ← overlaps task_a

    task_c = copy.copy(Task("Medication", 5, "high"))
    task_c.scheduled_time = "08:25"   # 08:25 – 08:30  ← also overlaps task_a

    conflict_dog.plan = [task_a, task_b, task_c]

    for t in conflict_dog.plan:
        end_min = Scheduler._to_minutes(t.scheduled_time) + t.duration_minutes
        end_str = Scheduler._minutes_to_time(end_min)
        print(f"   {t.scheduled_time}–{end_str}  {t.title}")

    print_warnings(conflict_dog.check_conflicts(), "Same-pet conflict check — Biscuit (forced)")

    # ── SCENARIO 3: Cross-pet conflict ────────────────────────────────
    # Both pets start at 08:00. Jordan can only do one thing at a time,
    # so overlapping tasks across pets are a real scheduling problem.
    print("\n\n── SCENARIO 3: Cross-pet conflict ──\n")
    print("   Both pets start at 08:00 — Jordan can't walk Biscuit")
    print("   and clean Mochi's litter box simultaneously.\n")

    # Give cat its own scheduler with a fresh owner budget
    cat_owner = Owner(name="Jordan", available_minutes=120, preferred_start="08:00")
    cat_owner.add_pet(cat)
    cat_sched = Scheduler(owner=cat_owner, pet=cat)
    cat_sched.add_task(Task("Litter box",  5, "high",   recurrence="daily"))
    cat_sched.add_task(Task("Feeding",    10, "high",   recurrence="daily"))
    cat_sched.add_task(Task("Playtime",   15, "medium", recurrence="daily"))
    cat_sched.build_plan()

    print("   Biscuit's plan:")
    for t in dog_sched.sort_by_time():
        end_min = Scheduler._to_minutes(t.scheduled_time) + t.duration_minutes
        print(f"     {t.scheduled_time}–{Scheduler._minutes_to_time(end_min)}  {t.title}")

    print("\n   Mochi's plan:")
    for t in cat_sched.sort_by_time():
        end_min = Scheduler._to_minutes(t.scheduled_time) + t.duration_minutes
        print(f"     {t.scheduled_time}–{Scheduler._minutes_to_time(end_min)}  {t.title}")

    cross_warnings = Scheduler.check_cross_pet_conflicts([dog_sched, cat_sched])
    print_warnings(cross_warnings, "Cross-pet conflict check — Biscuit vs Mochi")

    # ── SCENARIO 4: check_conflicts on empty plan ─────────────────────
    print("\n\n── SCENARIO 4: check_conflicts() before build_plan() ──\n")
    empty_sched = Scheduler(owner=owner, pet=dog)
    print("   (no build_plan() called — should return info warning, not crash)")
    print_warnings(empty_sched.check_conflicts(), "Empty plan check")

    print(f"\n{divider}")
    print("  Conflict detection verified — no crashes. 🐾")
    print(divider)


if __name__ == "__main__":
    main()