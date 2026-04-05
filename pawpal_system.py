from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    task_id: str
    pet_id: str
    name: str
    duration: int        # in minutes
    priority: str        # e.g. "high", "medium", "low"

    def add_task(self):
        pass

    def edit_task(self, name=None, duration=None, priority=None):
        pass


@dataclass
class Pet:
    pet_id: str
    owner_id: str
    name: str
    task_ids: List[str] = field(default_factory=list)


class Owner:
    def __init__(self, owner_id: str, time_available: int, priorities: List[str]):
        self.owner_id = owner_id
        self.time_available = time_available   # total minutes available per day
        self.priorities = priorities           # ordered list of priority labels
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def edit_pet(self, pet_id: str, **kwargs):
        pass


class Scheduler:
    def __init__(self, owner: Owner, tasks: List[Task]):
        self.time_constraints = owner.time_available
        self.priorities = owner.priorities
        self.tasks = tasks

    def generate_daily_plan(self) -> List[Task]:
        pass

    def display_plan(self, plan: List[Task]):
        pass

    def explain_reasoning(self, plan: List[Task]) -> str:
        pass
