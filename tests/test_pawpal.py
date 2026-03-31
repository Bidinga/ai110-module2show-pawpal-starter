import pytest
from datetime import datetime, date, time, timedelta
from pawpal_system import Task, Pet, TaskType, Priority, ScheduleManager, Owner


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


def test_sorting_correctness():
    owner = Owner(owner_id="o1", name="Owner")
    pet = Pet(pet_id="p1", name="Buddy", species="dog", age=4)
    owner.add_pet(pet)

    today = date.today()
    t_early = Task(
        task_id="s1",
        title="Early",
        task_type=TaskType.OTHER,
        priority=Priority.MEDIUM,
        start_time=datetime.combine(today, time(hour=7, minute=30)),
        duration_minutes=10,
    )
    t_late_high = Task(
        task_id="s2",
        title="Late High",
        task_type=TaskType.OTHER,
        priority=Priority.HIGH,
        start_time=datetime.combine(today, time(hour=8, minute=0)),
        duration_minutes=10,
    )
    t_late_critical = Task(
        task_id="s3",
        title="Late Critical",
        task_type=TaskType.OTHER,
        priority=Priority.CRITICAL,
        start_time=datetime.combine(today, time(hour=8, minute=0)),
        duration_minutes=5,
    )

    pet.assign_task(t_late_high)
    pet.assign_task(t_early)
    pet.assign_task(t_late_critical)

    mgr = ScheduleManager()
    mgr.ingest_owner(owner)

    agenda = mgr.get_daily_agenda(today)
    scheduled = [t for t in agenda if t.start_time]

    assert scheduled[0].start_time.time() == time(7, 30)
    # for the tied 08:00 tasks, CRITICAL (value=1) should come before HIGH (value=2)
    assert scheduled[1].start_time.time() == time(8, 0)
    assert scheduled[2].start_time.time() == time(8, 0)
    assert scheduled[1].priority.value < scheduled[2].priority.value


def test_recurrence_logic_preserved_for_next_day_after_completion():
    owner = Owner(owner_id="o2", name="Owner2")
    pet = Pet(pet_id="p2", name="Mochi", species="cat", age=3)
    owner.add_pet(pet)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    t = Task(
        task_id="r1",
        title="Daily Med",
        task_type=TaskType.MEDICATION,
        priority=Priority.CRITICAL,
        start_time=datetime.combine(today, time(hour=20, minute=0)),
        duration_minutes=5,
        is_recurring=True,
        recurrence="daily",
    )
    pet.assign_task(t)

    mgr = ScheduleManager()
    mgr.ingest_owner(owner)

    # mark the master copy as completed to simulate user marking today's occurrence done
    for mt in mgr.master_schedule:
        if mt.task_id == t.task_id:
            mt.mark_completed()

    # recurrence should still produce an occurrence for tomorrow (occurrence will reflect completion state)
    tomorrow_agenda = mgr.get_daily_agenda(tomorrow)
    occs = [x for x in tomorrow_agenda if x.task_id.startswith(f"{t.task_id}::occ::")]
    assert len(occs) == 1
    assert occs[0].start_time.date() == tomorrow


def test_conflict_detection_and_add_behavior():
    owner = Owner(owner_id="o3", name="Owner3")
    p1 = Pet(pet_id="pa", name="A", species="dog", age=2)
    p2 = Pet(pet_id="pb", name="B", species="cat", age=1)
    owner.add_pet(p1)
    owner.add_pet(p2)

    today = date.today()
    t1 = Task(
        task_id="c1",
        title="T1",
        task_type=TaskType.EXERCISE,
        priority=Priority.MEDIUM,
        start_time=datetime.combine(today, time(hour=9, minute=0)),
        duration_minutes=30,
    )
    p1.assign_task(t1)

    mgr = ScheduleManager()
    mgr.ingest_owner(owner)

    # new task that overlaps t1
    new_t = Task(
        task_id="c2",
        title="Overlap",
        task_type=TaskType.FEEDING,
        priority=Priority.HIGH,
        start_time=datetime.combine(today, time(hour=9, minute=15)),
        duration_minutes=15,
    )

    conflicts = mgr.detect_conflicts_for_task(new_t)
    assert len(conflicts) >= 1

    # reject when not allowed
    added = mgr.add_task_to_schedule(new_t, allow_conflict=False)
    assert not added

    # allow when forced
    added_forced = mgr.add_task_to_schedule(new_t, allow_conflict=True)
    assert added_forced
    assert any(t.task_id == new_t.task_id for t in mgr.master_schedule)
