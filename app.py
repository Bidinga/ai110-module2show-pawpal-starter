import streamlit as st
from pawpal_system import Owner, Pet, Task, TaskType, Priority, ScheduleManager
import uuid
from datetime import datetime, date, time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Session-managed Owner and Scheduler
if "owner" not in st.session_state:
    # create an Owner object and store it in session state
    st.session_state.owner = Owner(owner_id="owner1", name=owner_name)
else:
    # keep owner name in sync with the input
    st.session_state.owner.name = owner_name

if "scheduler" not in st.session_state:
    st.session_state.scheduler = ScheduleManager()

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Pet creation UI: add new pet to Owner
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    new_pet_name = st.text_input("New pet name", value=pet_name, key="new_pet_name")
with col_pet2:
    new_pet_species = st.selectbox("New pet species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet"):
    new_id = uuid.uuid4().hex[:8]
    pet = Pet(pet_id=new_id, name=new_pet_name, species=new_pet_species, age=1)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added pet {new_pet_name}")

# display current pets to choose when creating tasks
pets = st.session_state.owner.pets
if pets:
    pet_options = {f"{p.name} ({p.pet_id})": p.pet_id for p in pets}
    pet_choice_label = st.selectbox("Assign task to pet", options=list(pet_options.keys()))
    selected_pet_id = pet_options[pet_choice_label]
else:
    st.info("No pets yet — add one above before adding tasks.")
    selected_pet_id = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")

# additional task metadata: type and optional time
col_type, col_time = st.columns(2)
with col_type:
    task_type_str = st.selectbox("Task type", [t.value for t in TaskType], index=0, key="task_type")
with col_time:
    set_time = st.checkbox("Set time for task", value=False, key="set_time")
    if set_time:
        task_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=8, key="task_hour")
        task_min = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, key="task_min")

if st.button("Add task"):
    if not selected_pet_id:
        st.error("Please add a pet first and select it to assign the task.")
    else:
        # map priority string to Priority enum
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
        priority_enum = priority_map.get(priority_str, Priority.MEDIUM)
        # map task type string to TaskType
        type_map = {t.value: t for t in TaskType}
        task_type_enum = type_map.get(task_type_str, TaskType.OTHER)

        start_dt = None
        if set_time:
            start_dt = datetime.combine(date.today(), time(hour=int(task_hour), minute=int(task_min)))

        task_id = uuid.uuid4().hex[:8]
        task = Task(
            task_id=task_id,
            title=task_title,
            task_type=task_type_enum,
            priority=priority_enum,
            start_time=start_dt,
            duration_minutes=int(duration),
        )
        # assign to pet
        pet = st.session_state.owner.find_pet(selected_pet_id)
        if pet:
            pet.assign_task(task)
            # also add to scheduler
            st.session_state.scheduler.add_task_to_schedule(task)
            st.success(f"Added task '{task_title}' to {pet.name}.")
        else:
            st.error("Selected pet not found — try adding it again.")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"pet_id": p.pet_id, "name": p.name, "species": p.species} for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above.")

if any(p.tasks for p in st.session_state.owner.pets):
    st.write("Current tasks (per pet):")
    rows = []
    for p in st.session_state.owner.pets:
        for t in p.tasks:
            rows.append({"pet": p.name, "title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority.name})
    st.table(rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # regenerate scheduler view from owner tasks
    st.session_state.scheduler.clear()
    st.session_state.scheduler.ingest_owner(st.session_state.owner)
    today = date.today()
    agenda = st.session_state.scheduler.get_daily_agenda(today)
    if not agenda:
        st.info("No scheduled tasks for today.")
    else:
        # simple readable display
        for t in agenda:
            pet = st.session_state.owner.find_pet(t.pet_id) if t.pet_id else None
            pet_name = pet.name if pet else "(unknown)"
            if t.start_time and t.end_time:
                start = t.start_time.strftime("%H:%M")
                end = t.end_time.strftime("%H:%M")
                st.write(f"{start}-{end}: {t.title} [{pet_name}] — {t.task_type.value} — {t.priority.name}")
            else:
                st.write(f"(unscheduled) {t.title} [{pet_name}] — {t.task_type.value} — {t.priority.name}")
