from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner(owner_id="owner_1", time_available=90, priorities=["high", "medium", "low"])

# --- Setup Pets ---
buddy = Pet(pet_id="pet_1", owner_id="owner_1", name="Buddy")
luna  = Pet(pet_id="pet_2", owner_id="owner_1", name="Luna")

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Add Tasks ---
buddy.add_task(Task(task_id="t1", pet_id="pet_1", name="Morning Walk",   duration=30, priority="high",   frequency="daily"))
buddy.add_task(Task(task_id="t2", pet_id="pet_1", name="Flea Treatment", duration=15, priority="medium", frequency="weekly"))
luna.add_task( Task(task_id="t3", pet_id="pet_2", name="Feeding",        duration=10, priority="high",   frequency="daily"))
luna.add_task( Task(task_id="t4", pet_id="pet_2", name="Playtime",       duration=20, priority="low",    frequency="daily"))
luna.add_task( Task(task_id="t5", pet_id="pet_2", name="Vet Checkup",    duration=60, priority="medium", frequency="as_needed"))

# --- Run Scheduler ---
scheduler = Scheduler(owner)
plan = scheduler.generate_daily_plan()

print("=" * 45)
print("          Today's Schedule — PawPal+")
print("=" * 45)
scheduler.display_plan(plan)
print()
print(scheduler.explain_reasoning(plan))
