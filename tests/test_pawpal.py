import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def make_scheduler(time_available=120):
    owner = Owner(owner_id="o1", time_available=time_available, priorities=["high", "medium", "low"])
    pet = Pet(pet_id="pet_1", owner_id="o1", name="Buddy")
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


# --- Existing tests ---

def test_mark_complete_changes_status():
    task = Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(pet_id="pet_1", owner_id="o1", name="Buddy")
    assert len(pet.tasks) == 0
    pet.add_task(Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high"))
    assert len(pet.tasks) == 1


# --- Sorting Correctness ---

def test_sort_by_time_chronological_order():
    _, _, scheduler = make_scheduler()
    tasks = [
        Task(task_id="t3", pet_id="pet_1", name="Dinner", duration=10, priority="low", scheduled_time="18:00"),
        Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high", scheduled_time="07:00"),
        Task(task_id="t2", pet_id="pet_1", name="Meds", duration=5, priority="high", scheduled_time="12:00"),
    ]
    sorted_tasks = scheduler.sort_by_time(tasks)
    assert [t.scheduled_time for t in sorted_tasks] == ["07:00", "12:00", "18:00"]


def test_sort_by_time_does_not_mutate_original():
    _, _, scheduler = make_scheduler()
    tasks = [
        Task(task_id="t2", pet_id="pet_1", name="Dinner", duration=10, priority="low", scheduled_time="18:00"),
        Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high", scheduled_time="07:00"),
    ]
    original_order = [t.task_id for t in tasks]
    scheduler.sort_by_time(tasks)
    assert [t.task_id for t in tasks] == original_order


# --- Recurrence Logic ---

def test_complete_daily_task_creates_next_day_task():
    owner, pet, scheduler = make_scheduler()
    today = date.today()
    task = Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high",
                frequency="daily", due_date=today)
    pet.add_task(task)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.task_id == "t1_next"


def test_complete_weekly_task_creates_next_week_task():
    owner, pet, scheduler = make_scheduler()
    today = date.today()
    task = Task(task_id="t2", pet_id="pet_1", name="Bath", duration=30, priority="medium",
                frequency="weekly", due_date=today)
    pet.add_task(task)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_complete_as_needed_task_returns_none():
    owner, pet, scheduler = make_scheduler()
    task = Task(task_id="t3", pet_id="pet_1", name="Vet", duration=60, priority="high",
                frequency="as_needed")
    pet.add_task(task)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is None


def test_complete_daily_task_adds_to_pet():
    owner, pet, scheduler = make_scheduler()
    task = Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high",
                frequency="daily")
    pet.add_task(task)
    initial_count = len(pet.tasks)

    scheduler.complete_task(task)

    assert len(pet.tasks) == initial_count + 1


# --- Conflict Detection ---

def test_detect_conflicts_flags_same_time():
    owner, pet, scheduler = make_scheduler()
    tasks = [
        Task(task_id="t1", pet_id="pet_1", name="Walk", duration=30, priority="high", scheduled_time="08:00"),
        Task(task_id="t2", pet_id="pet_1", name="Meds", duration=15, priority="high", scheduled_time="08:00"),
    ]
    warnings = scheduler.detect_conflicts(tasks)
    assert len(warnings) == 1
    assert "WARNING" in warnings[0]


def test_detect_conflicts_flags_overlap():
    owner, pet, scheduler = make_scheduler()
    tasks = [
        Task(task_id="t1", pet_id="pet_1", name="Walk", duration=30, priority="high", scheduled_time="08:00"),
        Task(task_id="t2", pet_id="pet_1", name="Meds", duration=20, priority="high", scheduled_time="08:20"),
    ]
    warnings = scheduler.detect_conflicts(tasks)
    assert len(warnings) == 1


def test_detect_conflicts_no_overlap():
    owner, pet, scheduler = make_scheduler()
    tasks = [
        Task(task_id="t1", pet_id="pet_1", name="Walk", duration=30, priority="high", scheduled_time="08:00"),
        Task(task_id="t2", pet_id="pet_1", name="Meds", duration=15, priority="high", scheduled_time="09:00"),
    ]
    warnings = scheduler.detect_conflicts(tasks)
    assert warnings == []


def test_detect_conflicts_skips_completed_tasks():
    owner, pet, scheduler = make_scheduler()
    t1 = Task(task_id="t1", pet_id="pet_1", name="Walk", duration=30, priority="high", scheduled_time="08:00")
    t2 = Task(task_id="t2", pet_id="pet_1", name="Meds", duration=15, priority="high", scheduled_time="08:00")
    t1.mark_complete()
    warnings = scheduler.detect_conflicts([t1, t2])
    assert warnings == []


# --- Edge Cases ---

def test_pet_with_no_tasks_generates_empty_plan():
    owner, pet, scheduler = make_scheduler()
    plan = scheduler.generate_daily_plan()
    assert plan == []


def test_generate_plan_zero_time_available():
    owner, pet, scheduler = make_scheduler(time_available=0)
    pet.add_task(Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high"))
    plan = scheduler.generate_daily_plan()
    assert plan == []


def test_filter_by_pet_unknown_name_returns_empty():
    owner, pet, scheduler = make_scheduler()
    tasks = [Task(task_id="t1", pet_id="pet_1", name="Walk", duration=20, priority="high")]
    result = scheduler.filter_by_pet(tasks, "NonExistentPet")
    assert result == []
