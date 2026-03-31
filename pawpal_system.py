from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from typing import List, Optional


@dataclass
class Task:
    """Core data structure representing a pet care task."""

    task_id: str
    title: str
    task_type: str  # e.g., Feeding, Medication, Exercise, Appointment
    priority: int  # 1-Critical, 2-High, 3-Medium, 4-Low
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_recurring: bool = False
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def get_duration(self) -> Optional[timedelta]:
        """Return the duration (end_time - start_time) if both are set."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class Pet:
    """Represents a pet with basic profile and assigned tasks."""

    pet_id: str
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_details(self) -> str:
        """Return a short, formatted description of the pet."""
        return f"{self.name} ({self.species}), {self.age} yrs"

    def assign_task(self, task: Task) -> None:
        """Attach a Task to this pet."""
        self.tasks.append(task)


class Owner:
    """Represents the owner/user and manages their pets."""

    def __init__(self, owner_id: str, name: str):
        self.owner_id = owner_id
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet by id. Returns True if removed, False otherwise."""
        for i, p in enumerate(self.pets):
            if p.pet_id == pet_id:
                del self.pets[i]
                return True
        return False


class ScheduleManager:
    """Controller responsible for scheduling, conflict detection, and sorting."""

    def __init__(self):
        # master_schedule holds all tasks across owners/pets
        self.master_schedule: List[Task] = []

    def add_task_to_schedule(self, task: Task) -> bool:
        """Attempt to add a task after checking for conflicts.

        Returns True if the task was added, False otherwise.
        """
        # TODO: implement conflict checking and insertion logic
        raise NotImplementedError

    def detect_conflict(self, new_task: Task) -> bool:
        """Return True if new_task's time window overlaps any existing task."""
        # TODO: implement overlap logic comparing start_time/end_time
        raise NotImplementedError

    def get_daily_agenda(self, target_date: date) -> List[Task]:
        """Return all tasks scheduled for the provided date."""
        # TODO: filter master_schedule for tasks occurring on target_date
        raise NotImplementedError

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks chronologically by start_time; use priority as tie-breaker.

        Returns a new sorted list.
        """
        # TODO: implement sorting behavior
        raise NotImplementedError
