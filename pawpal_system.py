from dataclasses import dataclass, field
from datetime import datetime, timedelta, date, time
from typing import List, Optional
from enum import Enum
import copy


class TaskType(Enum):
    FEEDING = "Feeding"
    MEDICATION = "Medication"
    EXERCISE = "Exercise"
    APPOINTMENT = "Appointment"
    OTHER = "Other"


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class Task:
    """Represents a single pet care activity.

    Recurrence is a simple model: None for one-off, 'daily' or 'weekly' for simple rules.
    """

    task_id: str
    title: str
    task_type: TaskType
    priority: Priority
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    is_recurring: bool = False
    recurrence: Optional[str] = None  # None | 'daily' | 'weekly'
    pet_id: Optional[str] = None
    is_completed: bool = False

    def __post_init__(self):
        """Derive end_time from duration when start_time is provided."""
        # Derive end_time from duration if needed
        if self.duration_minutes is not None and self.start_time and not self.end_time:
            self.end_time = self.start_time + timedelta(minutes=self.duration_minutes)

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def get_duration(self) -> Optional[timedelta]:
        """Return the task duration as a timedelta when available."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        if self.duration_minutes is not None:
            return timedelta(minutes=self.duration_minutes)
        return None

    def overlaps_with(self, other: "Task") -> bool:
        """Return True if time windows overlap. Tasks without times do not overlap."""
        if not self.start_time or not self.end_time or not other.start_time or not other.end_time:
            return False
        return (self.start_time < other.end_time) and (other.start_time < self.end_time)

    def occurs_on(self, target_date: date) -> bool:
        """Return True if this task (or an occurrence of it when recurring) falls on target_date."""
        if self.start_time and self.start_time.date() == target_date:
            return True
        if self.is_recurring and self.start_time:
            if self.recurrence == "daily" and self.start_time.date() <= target_date:
                return True
            if self.recurrence == "weekly" and self.start_time.date() <= target_date:
                # same weekday
                return self.start_time.weekday() == target_date.weekday()
        return False

    def occurrence_for_date(self, target_date: date) -> Optional["Task"]:
        """If the task occurs on target_date, return a shallow copy with start/end adjusted to target_date.

        For one-off tasks this returns self if the date matches. For recurring tasks, this returns
        a copy representing that day's occurrence (task_id preserved with suffix).
        """
        if not self.occurs_on(target_date):
            return None

        if not self.is_recurring:
            # one-off
            return self

        # build occurrence preserving time-of-day and duration
        if not self.start_time:
            return None

        st_time: time = self.start_time.time()
        duration = self.get_duration()
        occ_start = datetime.combine(target_date, st_time)
        occ_end = occ_start + duration if duration else None

        occ = copy.copy(self)
        occ.start_time = occ_start
        occ.end_time = occ_end
        # indicate this is an occurrence instance
        occ.task_id = f"{self.task_id}::occ::{target_date.isoformat()}"
        return occ


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_details(self) -> str:
        """Return a short, formatted description of the pet."""
        return f"{self.name} ({self.species}), {self.age} yrs"

    def assign_task(self, task: Task) -> None:
        """Assign a Task to this pet and set the task.pet_id."""
        task.pet_id = self.pet_id
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the pet by its id."""
        for i, t in enumerate(self.tasks):
            if t.task_id == task_id:
                del self.tasks[i]
                return True
        return False

    def list_tasks(self) -> List[Task]:
        """Return a shallow list of this pet's tasks."""
        return list(self.tasks)


class Owner:
    def __init__(self, owner_id: str, name: str):
        """Create an Owner with the given id and name."""
        self.owner_id = owner_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to this Owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a Pet by id from this Owner."""
        for i, p in enumerate(self.pets):
            if p.pet_id == pet_id:
                del self.pets[i]
                return True
        return False

    def find_pet(self, pet_id: str) -> Optional[Pet]:
        """Return the Pet with the given id, or None if not found."""
        for p in self.pets:
            if p.pet_id == pet_id:
                return p
        return None

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this Owner."""
        tasks: List[Task] = []
        for p in self.pets:
            tasks.extend(p.list_tasks())
        return tasks


class ScheduleManager:
    """Central scheduler that manages a master schedule and provides agenda views."""

    def __init__(self):
        """Initialize the ScheduleManager with an empty master schedule."""
        self.master_schedule: List[Task] = []

    def ingest_owner(self, owner: Owner) -> None:
        """Load all tasks from an Owner's pets into the master schedule.

        This does not deduplicate by id; callers should ensure they don't ingest the same owner twice.
        """
        for t in owner.list_all_tasks():
            # shallow copy to keep master_schedule independent
            self.master_schedule.append(copy.copy(t))
        # keep sorted for faster operations
        self.master_schedule.sort(key=lambda t: (t.start_time or datetime.max))

    def add_task_to_schedule(self, task: Task, allow_conflict: bool = False) -> bool:
        """Add a task if it does not conflict (unless allow_conflict=True).

        Returns True if added, False if rejected due to conflict.
        """
        if not task.start_time or not task.end_time:
            self.master_schedule.append(copy.copy(task))
            return True

        if not allow_conflict and self.detect_conflict(task):
            return False

        self.master_schedule.append(copy.copy(task))
        self.master_schedule.sort(key=lambda t: (t.start_time or datetime.max))
        return True

    def detect_conflict(self, new_task: Task) -> bool:
        """Detect if new_task overlaps with any existing scheduled task.

        Policy: conflicts are global (owner is single resource). This can be changed later.
        """
        if not new_task.start_time or not new_task.end_time:
            return False
        for t in self.master_schedule:
            if t.start_time and t.end_time and (t.start_time < new_task.end_time) and (new_task.start_time < t.end_time):
                return True
        return False

    def get_daily_agenda(self, target_date: date) -> List[Task]:
        """Return concrete Task objects representing what happens on target_date.

        Recurring tasks are expanded into occurrence instances for that date.
        Unscheduled tasks are returned at the end of the list.
        """
        occurrences: List[Task] = []
        backlog: List[Task] = []
        for t in self.master_schedule:
            if t.start_time:
                occ = t.occurrence_for_date(target_date)
                if occ:
                    occurrences.append(occ)
            else:
                backlog.append(copy.copy(t))

        sorted_occ = self.sort_tasks(occurrences)
        return sorted_occ + backlog

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by start time (earlier first) then by priority."""
        def key_fn(t: Task):
            st = t.start_time if t.start_time is not None else datetime.max
            # lower enum value => higher urgency (CRITICAL=1)
            return (st, t.priority.value)

        return sorted(tasks, key=key_fn)

    # utility mutators
    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the master schedule by its id."""
        for i, t in enumerate(self.master_schedule):
            if t.task_id == task_id:
                del self.master_schedule[i]
                return True
        return False

    def update_task(self, task_id: str, **fields) -> bool:
        """Update fields on a task in the master schedule; returns True if updated."""
        for t in self.master_schedule:
            if t.task_id == task_id:
                for k, v in fields.items():
                    if hasattr(t, k):
                        setattr(t, k, v)
                # recompute derived values
                if t.duration_minutes is not None and t.start_time and not t.end_time:
                    t.end_time = t.start_time + timedelta(minutes=t.duration_minutes)
                return True
        return False

    def list_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Return tasks in the master schedule belonging to the given pet id."""
        return [t for t in self.master_schedule if t.pet_id == pet_id]

    def clear(self) -> None:
        """Remove all tasks from the master schedule."""
        self.master_schedule.clear()
