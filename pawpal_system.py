from dataclasses import dataclass, field
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
