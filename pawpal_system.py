from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from typing import List, Optional


@dataclass
class Task:
    task_id: str
    pet_id: str
    name: str
    duration: int               # in minutes
    priority: str               # "high", "medium", "low"
    frequency: str = "daily"    # "daily", "weekly", "as_needed"
    completed: bool = False
    scheduled_time: str = "00:00"  # "HH:MM" format, e.g. "08:30"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Reset this task to incomplete."""
        self.completed = False


@dataclass
class Pet:
    pet_id: str
    owner_id: str
    name: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def edit_task(self, task_id: str, **kwargs):
        """Update fields on an existing task by task_id."""
        for task in self.tasks:
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return
        raise ValueError(f"Task '{task_id}' not found on pet '{self.pet_id}'")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Return the Task with the given task_id, or None if not found."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None


class Owner:
    def __init__(self, owner_id: str, time_available: int, priorities: List[str]):
        self.owner_id = owner_id
        self.time_available = time_available   # total minutes available per day
        self.priorities = priorities           # ordered list of priority labels
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's pet list."""
        self.pets.append(pet)

    def edit_pet(self, pet_id: str, **kwargs):
        """Update fields on an existing pet by pet_id."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                for key, value in kwargs.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)
                return
        raise ValueError(f"Pet '{pet_id}' not found for owner '{self.owner_id}'")

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Return the Pet with the given pet_id, or None if not found."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across every pet."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner):
        self.owner = owner                     # keep live reference, not a copy

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort a list of tasks into chronological order by scheduled_time.

        Uses Python's built-in sorted() with a lambda key. Because scheduled_time
        is stored as a zero-padded 'HH:MM' string, plain string comparison produces
        correct chronological ordering without parsing — '07:00' < '08:30' < '18:00'.

        Args:
            tasks: The list of Task objects to sort. The original list is not modified.

        Returns:
            A new list of Task objects ordered earliest scheduled_time first.
        """
        return sorted(tasks, key=lambda t: t.scheduled_time)

    def filter_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Filter tasks by their completion status.

        Args:
            tasks: The list of Task objects to filter.
            completed: Pass True to keep only finished tasks,
                       False to keep only tasks still pending.

        Returns:
            A new list containing only the tasks whose completed flag
            matches the given value.
        """
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks so only those belonging to a specific pet are returned.

        Builds a set of matching pet_ids first (O(p) where p = number of pets),
        then filters in a single pass over tasks (O(t)), making the overall
        complexity O(p + t) rather than O(p * t).

        Args:
            tasks: The list of Task objects to filter.
            pet_name: The pet's display name. Matching is case-insensitive,
                      so 'buddy' and 'Buddy' are treated as the same pet.

        Returns:
            A new list of Task objects assigned to the named pet.
            Returns an empty list if no pet with that name exists.
        """
        matching_ids = {
            p.pet_id for p in self.owner.pets
            if p.name.lower() == pet_name.lower()
        }
        return [t for t in tasks if t.pet_id in matching_ids]

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and auto-schedule the next occurrence for recurring tasks.

        For tasks with frequency 'daily' or 'weekly', a new Task instance is
        created with the same attributes and a due_date advanced by 1 or 7 days
        respectively (calculated with datetime.timedelta). The new task is
        immediately registered on the owning pet so it appears in future plans.

        Tasks with frequency 'as_needed' are simply marked complete; no follow-up
        task is created.

        Args:
            task: The Task to complete. Its completed flag is set to True in-place.

        Returns:
            The newly created next-occurrence Task if the task is recurring,
            or None if frequency is 'as_needed'.
        """
        task.mark_complete()

        if task.frequency not in ("daily", "weekly"):
            return None

        # timedelta calculates the next due date precisely:
        # daily → today + 1 day, weekly → today + 7 days
        days_ahead = 1 if task.frequency == "daily" else 7
        next_due = task.due_date + timedelta(days=days_ahead)

        next_task = Task(
            task_id=f"{task.task_id}_next",
            pet_id=task.pet_id,
            name=task.name,
            duration=task.duration,
            priority=task.priority,
            frequency=task.frequency,
            scheduled_time=task.scheduled_time,
            due_date=next_due,
        )

        pet = self.owner.get_pet(task.pet_id)
        if pet:
            pet.add_task(next_task)

        return next_task

    @staticmethod
    def _to_minutes(hhmm: str) -> int:
        """Convert a 'HH:MM' time string to an integer number of minutes from midnight.

        Used internally by detect_conflicts to compare task windows numerically.

        Args:
            hhmm: A zero-padded time string in 'HH:MM' format, e.g. '08:30'.

        Returns:
            Total minutes from midnight as an int. '08:30' → 510, '18:00' → 1080.
        """
        h, m = hhmm.split(":")
        return int(h) * 60 + int(m)

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect scheduling conflicts among incomplete tasks and return human-readable warnings.

        Uses itertools.combinations to check every pair of incomplete tasks exactly once.
        Two tasks conflict when their scheduled time windows overlap, i.e.:
            task_a starts before task_b ends  AND  task_b starts before task_a ends.

        This is a lightweight O(n²) pairwise scan — acceptable because a typical daily
        pet schedule has a small number of tasks. The method never raises; callers always
        receive a list (empty = no conflicts).

        Args:
            tasks: The list of Task objects to check. Completed tasks are ignored.

        Returns:
            A list of warning strings, one per conflicting pair, in the format:
            "WARNING: '<name_a>' (<pet_a>, HH:MM for N min) overlaps with '<name_b>' (...)".
            Returns an empty list if no conflicts are found.
        """
        warnings = []
        incomplete = [t for t in tasks if not t.completed]

        for a, b in combinations(incomplete, 2):
            a_start = self._to_minutes(a.scheduled_time)
            a_end   = a_start + a.duration
            b_start = self._to_minutes(b.scheduled_time)
            b_end   = b_start + b.duration

            # Overlap condition: one window starts before the other ends
            if a_start < b_end and b_start < a_end:
                pet_a = self.owner.get_pet(a.pet_id)
                pet_b = self.owner.get_pet(b.pet_id)
                warnings.append(
                    f"WARNING: '{a.name}' ({pet_a.name if pet_a else a.pet_id}, "
                    f"{a.scheduled_time} for {a.duration} min) overlaps with "
                    f"'{b.name}' ({pet_b.name if pet_b else b.pet_id}, "
                    f"{b.scheduled_time} for {b.duration} min)"
                )
        return warnings

    def generate_daily_plan(self) -> List[Task]:
        """Return a priority-sorted list of tasks that fit within the owner's available time."""
        tasks = [t for t in self.owner.all_tasks() if not t.completed]
        tasks.sort(key=lambda t: self.PRIORITY_ORDER.get(t.priority, 99))

        plan = []
        time_used = 0
        for task in tasks:
            if time_used + task.duration <= self.owner.time_available:
                plan.append(task)
                time_used += task.duration

        return plan

    def display_plan(self, plan: List[Task]):
        """Print the daily plan to the terminal in a readable format."""
        if not plan:
            print("No tasks scheduled for today.")
            return

        total = sum(t.duration for t in plan)
        print(f"Daily Plan ({total} min / {self.owner.time_available} min available)")
        print("-" * 45)
        for task in plan:
            pet = self.owner.get_pet(task.pet_id)
            pet_name = pet.name if pet else task.pet_id
            status = "[x]" if task.completed else "[ ]"
            print(f"{status} [{task.priority.upper()}] {pet_name} — {task.name} ({task.duration} min)")

    def explain_reasoning(self, plan: List[Task]) -> str:
        """Return a plain-English summary of why tasks were included or skipped."""
        if not plan:
            return "No tasks fit within the available time."

        total = sum(t.duration for t in plan)
        skipped = [t for t in self.owner.all_tasks() if t not in plan and not t.completed]

        lines = [
            f"Scheduled {len(plan)} task(s) using {total} of {self.owner.time_available} available minutes.",
            f"Tasks are ordered by priority: {', '.join(self.owner.priorities)}.",
        ]
        if skipped:
            lines.append(f"Skipped {len(skipped)} task(s) due to time constraints: "
                         + ", ".join(t.name for t in skipped) + ".")
        return " ".join(lines)
