"""
PawPal+ — main.py
Demo script: creates an Owner, two Pets, adds tasks, prints Today's Schedule.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # ── 1. Create Owner ───────────────────────────────────────────────
    owner = Owner(
        name="Jordan",
        available_minutes=120,
        preferred_start="08:00",
    )

    # ── 2. Create two Pets and register them ──────────────────────────
    dog = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    cat = Pet(name="Mochi",   species="cat", breed="Siamese",          age=5)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # ── 3. Add tasks to Biscuit (dog) ─────────────────────────────────
    dog_scheduler = Scheduler(owner=owner, pet=dog)

    dog_scheduler.add_task(Task("Morning walk",   30, "high",   recurrence="daily"))
    dog_scheduler.add_task(Task("Feeding",        10, "high",   recurrence="daily"))
    dog_scheduler.add_task(Task("Medication",      5, "high",   recurrence="daily"))
    dog_scheduler.add_task(Task("Teeth brushing", 10, "medium", recurrence="daily"))
    dog_scheduler.add_task(Task("Enrichment toy", 15, "medium", recurrence="daily"))
    dog_scheduler.add_task(Task("Bath",           40, "low",    recurrence="weekly"))

    # ── 4. Add tasks to Mochi (cat) ───────────────────────────────────
    cat_scheduler = Scheduler(owner=owner, pet=cat)

    cat_scheduler.add_task(Task("Feeding",         10, "high",   recurrence="daily"))
    cat_scheduler.add_task(Task("Litter box",       5, "high",   recurrence="daily"))
    cat_scheduler.add_task(Task("Playtime",        15, "medium", recurrence="daily"))
    cat_scheduler.add_task(Task("Brush coat",      10, "medium", recurrence="weekly"))
    cat_scheduler.add_task(Task("Vet check-up",    30, "low",    recurrence="as_needed"))

    # ── 5. Build plans ────────────────────────────────────────────────
    dog_scheduler.build_plan()
    cat_scheduler.build_plan()

    # ── 6. Print Today's Schedule ─────────────────────────────────────
    divider = "=" * 52

    print(divider)
    print("        🐾  PawPal+ — Today's Schedule  🐾")
    print(divider)
    print(f"  Owner : {owner.name}")
    print(f"  Budget: {owner.available_minutes} min  |  Start: {owner.preferred_start}")
    print(divider)

    print()
    print(dog_scheduler.display_schedule())
    print()
    print(dog_scheduler.explain_plan())

    print()
    print(divider)

    print()
    print(cat_scheduler.display_schedule())
    print()
    print(cat_scheduler.explain_plan())

    print()
    print(divider)
    print("  All schedules generated. Have a great day! 🐶🐱")
    print(divider)


if __name__ == "__main__":
    main()