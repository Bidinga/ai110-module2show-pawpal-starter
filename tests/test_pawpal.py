import pytest
from datetime import datetime
from pawpal_system import Task, Pet, TaskType, Priority


def test_task_mark_completed():
    t = Task(task_id="t1", title="Test Task", task_type=TaskType.OTHER, priority=Priority.LOW)
    assert not t.is_completed
    t.mark_completed()
    assert t.is_completed


def test_pet_add_task_increases_count():
    p = Pet(pet_id="p1", name="Fido", species="dog", age=2)
    assert len(p.tasks) == 0
    t = Task(
        task_id="t2",
        title="Walk",
        task_type=TaskType.EXERCISE,
        priority=Priority.MEDIUM,
        start_time=datetime.now(),
        duration_minutes=15,
    )
    p.assign_task(t)
    assert len(p.tasks) == 1
    # ensure task.pet_id was set
    assert p.tasks[0].pet_id == p.pet_id
