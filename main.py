from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner(owner_id="owner_1", time_available=120, priorities=["high", "medium", "low"])

# --- Setup Pets ---
buddy = Pet(pet_id="pet_1", owner_id="owner_1", name="Buddy")
luna  = Pet(pet_id="pet_2", owner_id="owner_1", name="Luna")

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Add Tasks OUT OF ORDER (intentionally scrambled scheduled_time) ---
buddy.add_task(Task(task_id="t1", pet_id="pet_1", name="Evening Walk",   duration=30, priority="high",   frequency="daily",     scheduled_time="18:00"))
buddy.add_task(Task(task_id="t2", pet_id="pet_1", name="Flea Treatment", duration=15, priority="medium", frequency="weekly",    scheduled_time="14:00"))
buddy.add_task(Task(task_id="t3", pet_id="pet_1", name="Morning Walk",   duration=30, priority="high",   frequency="daily",     scheduled_time="07:00"))
luna.add_task( Task(task_id="t4", pet_id="pet_2", name="Feeding",        duration=10, priority="high",   frequency="daily",     scheduled_time="08:00"))
luna.add_task( Task(task_id="t5", pet_id="pet_2", name="Vet Checkup",    duration=60, priority="medium", frequency="as_needed", scheduled_time="10:30"))
luna.add_task( Task(task_id="t6", pet_id="pet_2", name="Playtime",       duration=20, priority="low",    frequency="daily",     scheduled_time="15:00"))

scheduler = Scheduler(owner)
all_tasks = owner.all_tasks()

# --- Demo 1: Sort by time ---
print("=" * 45)
print("  All Tasks — Sorted by Scheduled Time")
print("=" * 45)
for t in scheduler.sort_by_time(all_tasks):
    pet = owner.get_pet(t.pet_id)
    print(f"  {t.scheduled_time}  [{t.priority.upper():6}]  {pet.name:6} — {t.name} ({t.duration} min)")

# --- Demo 2: Filter by pet ---
print()
print("=" * 45)
print("  Buddy's Tasks Only (filter_by_pet)")
print("=" * 45)
for t in scheduler.filter_by_pet(all_tasks, "Buddy"):
    print(f"  {t.scheduled_time}  {t.name} ({t.priority})")

# --- Demo 3: Filter by completion status ---
print()
print("=" * 45)
print("  Incomplete Tasks Only (filter_by_status)")
print("=" * 45)
incomplete = scheduler.filter_by_status(all_tasks, completed=False)
for t in incomplete:
    pet = owner.get_pet(t.pet_id)
    print(f"  {pet.name:6} — {t.name} [done={t.completed}]")

# mark one complete and re-filter
all_tasks[0].mark_complete()
print()
print(f"  (Marked '{all_tasks[0].name}' complete — re-filtering...)")
print()
for t in scheduler.filter_by_status(all_tasks, completed=False):
    pet = owner.get_pet(t.pet_id)
    print(f"  {pet.name:6} — {t.name} [done={t.completed}]")

# --- Demo 4: Recurring task automation ---
print()
print("=" * 45)
print("  Recurring Task Demo (complete_task)")
print("=" * 45)
morning_walk = buddy.get_task("t3")  # Morning Walk — daily
print(f"  Before: '{morning_walk.name}' due {morning_walk.due_date}, completed={morning_walk.completed}")

next_occurrence = scheduler.complete_task(morning_walk)
print(f"  After:  '{morning_walk.name}' completed={morning_walk.completed}")
if next_occurrence:
    print(f"  Next:   '{next_occurrence.name}' auto-created for {next_occurrence.due_date} "
          f"(today + 1 day = {date.today()} + 1)")

# weekly task
flea = buddy.get_task("t2")  # Flea Treatment — weekly
next_flea = scheduler.complete_task(flea)
if next_flea:
    print(f"  Next:   '{next_flea.name}' (weekly) auto-created for {next_flea.due_date} "
          f"(today + 7 days)")

# as_needed task — should NOT spawn a new one
vet = luna.get_task("t5")
result = scheduler.complete_task(vet)
print(f"  '{vet.name}' (as_needed) spawned new task: {result is not None}  ← expected False")

# --- Demo 5: Conflict detection ---
print()
print("=" * 45)
print("  Conflict Detection Demo (detect_conflicts)")
print("=" * 45)

# Add two tasks that intentionally overlap:
# Buddy's Bath starts at 07:00 for 30 min → window 07:00–07:30
# Morning Walk_next also starts at 07:00 for 30 min → window 07:00–07:30
buddy.add_task(Task(
    task_id="t_conflict",
    pet_id="pet_1",
    name="Bath Time",
    duration=30,
    priority="medium",
    frequency="as_needed",
    scheduled_time="07:00",   # same window as Morning Walk_next
))
print("  Added 'Bath Time' for Buddy at 07:00 (30 min) — conflicts with Morning Walk_next (07:00, 30 min)")
print()

all_tasks_now = owner.all_tasks()
conflicts = scheduler.detect_conflicts(all_tasks_now)

if conflicts:
    for msg in conflicts:
        print(f"  {msg}")
else:
    print("  No conflicts detected.")

# --- Demo 7: Full schedule ---
print()
print("=" * 45)
print("      Today's Schedule — PawPal+")
print("=" * 45)
plan = scheduler.generate_daily_plan()
scheduler.display_plan(plan)
print()
print(scheduler.explain_reasoning(plan))
