import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session-state init ────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id="owner_1",
        time_available=480,
        priorities=["high", "medium", "low"],
    )
if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 0
if "task_counter" not in st.session_state:
    st.session_state.task_counter = 0

owner: Owner = st.session_state.owner

# ── Owner Settings ────────────────────────────────────────────────────────────
st.subheader("Owner Settings")
col_a, col_b = st.columns(2)
with col_a:
    st.text_input("Owner name", value="Jordan")
with col_b:
    owner.time_available = st.number_input(
        "Time available today (minutes)", min_value=1, max_value=1440, value=owner.time_available
    )

st.divider()

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    st.session_state.pet_counter += 1
    owner.add_pet(Pet(
        pet_id=f"pet_{st.session_state.pet_counter}",
        owner_id=owner.owner_id,
        name=pet_name,
    ))
    st.success(f"Added {pet_name}")

if owner.pets:
    st.table([{"name": p.name, "pet_id": p.pet_id} for p in owner.pets])
else:
    st.info("No pets yet.")

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

if not owner.pets:
    st.warning("Add a pet first.")
else:
    pet_options = {p.name: p for p in owner.pets}
    selected_pet_name = st.selectbox("Assign to pet", list(pet_options.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as_needed"])
    with col5:
        scheduled_time = st.text_input("Scheduled time (HH:MM)", value="08:00")

    if st.button("Add task"):
        st.session_state.task_counter += 1
        pet_options[selected_pet_name].add_task(Task(
            task_id=f"task_{st.session_state.task_counter}",
            pet_id=pet_options[selected_pet_name].pet_id,
            name=task_title,
            duration=int(duration),
            priority=priority,
            frequency=frequency,
            scheduled_time=scheduled_time,
        ))
        st.success(f"Added '{task_title}' to {selected_pet_name}")

    st.divider()

    # ── Filter & Sort Controls ────────────────────────────────────────────────
    all_tasks = owner.all_tasks()
    if all_tasks:
        scheduler = Scheduler(owner)

        st.subheader("View Tasks")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
        with col_f2:
            filter_status = st.selectbox("Filter by status", ["All", "Incomplete", "Complete"])
        with col_f3:
            sort_mode = st.selectbox("Sort by", ["Time", "Priority"])

        filtered = all_tasks
        if filter_pet != "All":
            filtered = scheduler.filter_by_pet(filtered, filter_pet)
        if filter_status == "Incomplete":
            filtered = scheduler.filter_by_status(filtered, completed=False)
        elif filter_status == "Complete":
            filtered = scheduler.filter_by_status(filtered, completed=True)

        if sort_mode == "Time":
            filtered = scheduler.sort_by_time(filtered)
        else:
            filtered = sorted(filtered, key=lambda t: scheduler.PRIORITY_ORDER.get(t.priority, 99))

        # Live conflict check on all tasks
        conflicts = scheduler.detect_conflicts(all_tasks)
        if conflicts:
            st.error(f"⚠️ {len(conflicts)} scheduling conflict(s) detected!")
            with st.expander("View conflicts"):
                for msg in conflicts:
                    # Strip the leading "WARNING: " prefix for cleaner display
                    st.warning(msg.replace("WARNING: ", ""))

        if filtered:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            st.table([
                {
                    "time": t.scheduled_time,
                    "pet": owner.get_pet(t.pet_id).name if owner.get_pet(t.pet_id) else t.pet_id,
                    "task": t.name,
                    "duration (min)": t.duration,
                    "priority": priority_emoji.get(t.priority, "") + " " + t.priority,
                    "frequency": t.frequency,
                    "done": "✅" if t.completed else "⬜",
                }
                for t in filtered
            ])
        else:
            st.info("No tasks match the current filters.")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()

    if plan:
        conflicts = scheduler.detect_conflicts(plan)
        if conflicts:
            st.error(f"⚠️ {len(conflicts)} conflict(s) in your schedule — tasks overlap in time!")
            for msg in conflicts:
                st.warning(msg.replace("WARNING: ", ""))
        else:
            st.success("No conflicts detected — your schedule looks good!")

        st.info(scheduler.explain_reasoning(plan))
        st.table([
            {
                "time": t.scheduled_time,
                "pet": owner.get_pet(t.pet_id).name if owner.get_pet(t.pet_id) else t.pet_id,
                "task": t.name,
                "duration (min)": t.duration,
                "priority": t.priority,
            }
            for t in scheduler.sort_by_time(plan)
        ])
    else:
        st.warning("No tasks could be scheduled.")

st.divider()

# ── Complete a Task ───────────────────────────────────────────────────────────
st.subheader("Complete a Task")

incomplete_tasks = [t for t in owner.all_tasks() if not t.completed]
if not incomplete_tasks:
    st.info("No incomplete tasks.")
else:
    scheduler = Scheduler(owner)
    task_labels = {
        f"{owner.get_pet(t.pet_id).name if owner.get_pet(t.pet_id) else t.pet_id} — {t.name} ({t.scheduled_time})": t
        for t in incomplete_tasks
    }
    selected_label = st.selectbox("Mark complete", list(task_labels.keys()))
    if st.button("Complete task"):
        done_task = task_labels[selected_label]
        next_t = scheduler.complete_task(done_task)
        st.success(f"Marked '{done_task.name}' complete.")
        if next_t:
            st.info(f"Next '{next_t.name}' auto-scheduled for {next_t.due_date}.")
