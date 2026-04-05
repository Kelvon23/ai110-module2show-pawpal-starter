import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(pet_id="pet_1", owner_id="owner_1", name="Buddy")
    assert len(pet.tasks) == 0
    pet.add_task(Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high"))
    assert len(pet.tasks) == 1
