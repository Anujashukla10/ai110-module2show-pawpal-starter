"""
PawPal+ — test suite
Run with: python -m pytest
"""

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """Task.mark_complete() should flip completed from False to True."""
    task = Task(title="Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False   # starts incomplete

    task.mark_complete()

    assert task.completed is True    # now complete


def test_add_task_increases_pet_task_count():
    """Pet.add_task() should increase the pet's task count by 1."""
    pet = Pet(name="Biscuit", species="dog")

    assert len(pet.get_tasks()) == 0   # starts with no tasks

    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    assert len(pet.get_tasks()) == 1   # now has one task