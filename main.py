from datetime import datetime, date, time, timedelta
from pawpal_system import Owner, Pet, Task, TaskType, Priority, ScheduleManager


def print_schedule_table(agenda, owner):
    cols = ["Time", "Duration", "Task", "Pet", "Type", "Priority", "Recurring", "Status"]
    widths = [13, 8, 28, 12, 12, 8, 9, 10]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)

    print(fmt.format(*cols))
    print("-" * (sum(widths) + 2 * (len(widths)-1)))

    for t in agenda:
        pet = owner.find_pet(t.pet_id) if t.pet_id else None
        pet_name = pet.name if pet else "(unknown)"
        if t.start_time and t.end_time:
            time_str = f"{t.start_time.strftime('%H:%M')}-{t.end_time.strftime('%H:%M')}"
        else:
            time_str = "(unscheduled)"
        duration = t.get_duration()
        dur_str = f"{int(duration.total_seconds()//60)}m" if duration else ""
        recur = "yes" if t.is_recurring else "no"
        status = "done" if t.is_completed else "pending"
        print(fmt.format(time_str, dur_str, (t.title or '')[:28], pet_name[:12], (t.task_type.value or '')[:12],
                         t.priority.name, recur, status))


def main():
    # Create owner and pets
    owner = Owner(owner_id="owner1", name="Jordan")
    pet1 = Pet(pet_id="pet1", name="Mochi", species="dog", age=3)
    pet2 = Pet(pet_id="pet2", name="Nala", species="cat", age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    today = date.today()

    # Create tasks and assign to pets
    t1 = Task(
        task_id="t1",
        title="Morning Walk",
        task_type=TaskType.EXERCISE,
        priority=Priority.HIGH,
        start_time=datetime.combine(today, time(hour=8, minute=0)),
        duration_minutes=30,
    )
    pet1.assign_task(t1)

    t2 = Task(
        task_id="t2",
        title="Breakfast",
        task_type=TaskType.FEEDING,
        priority=Priority.MEDIUM,
        start_time=datetime.combine(today, time(hour=7, minute=30)),
        duration_minutes=15,
    )
    pet2.assign_task(t2)

    t3 = Task(
        task_id="t3",
        title="Evening Medication",
        task_type=TaskType.MEDICATION,
        priority=Priority.CRITICAL,
        start_time=datetime.combine(today, time(hour=20, minute=0)),
        duration_minutes=5,
        is_recurring=True,
        recurrence="daily",
    )
    pet1.assign_task(t3)

    # Also add an unscheduled task
    t4 = Task(
        task_id="t4",
        title="Buy treats",
        task_type=TaskType.OTHER,
        priority=Priority.LOW,
    )
    pet2.assign_task(t4)

    # Create scheduler and ingest owner's tasks
    scheduler = ScheduleManager()
    scheduler.ingest_owner(owner)

    # Print today's schedule
    print(f"Today's Schedule ({today.isoformat()}):\n")
    agenda = scheduler.get_daily_agenda(today)

    if not agenda:
        print("  No tasks for today.")
        return

    # replaced manual loop with helper
    print_schedule_table(agenda, owner)


if __name__ == "__main__":
    main()
