"""
PawPal+ — app.py
Streamlit UI connected to pawpal_system.py backend.
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A daily care planner for your pets.")

# ─────────────────────────────────────────────
# Step 1 — Seed session_state with persistent objects
#
# Streamlit reruns the whole script on every interaction.
# We guard each key with `if key not in st.session_state`
# so objects are created ONCE and survive every rerun.
# ─────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = None          # set when the owner form is submitted

if "schedulers" not in st.session_state:
    st.session_state.schedulers = {}       # {pet_name: Scheduler}

# ─────────────────────────────────────────────
# Section 1 — Owner setup
# ─────────────────────────────────────────────

st.header("1 · Owner Info")

with st.form("owner_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        owner_name = st.text_input("Your name", value="Jordan")
    with col2:
        available_minutes = st.number_input(
            "Time available today (min)", min_value=10, max_value=480, value=120
        )
    with col3:
        preferred_start = st.text_input("Start time (HH:MM)", value="08:00")

    submitted_owner = st.form_submit_button("Save owner")

if submitted_owner:
    # Create (or replace) the Owner object and clear any existing schedulers
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=int(available_minutes),
        preferred_start=preferred_start,
    )
    st.session_state.schedulers = {}
    st.success(f"Owner **{owner_name}** saved — {available_minutes} min starting {preferred_start}.")

# Show current owner if one exists
if st.session_state.owner:
    o = st.session_state.owner
    st.info(f"👤 **{o.name}** · {o.available_minutes} min/day · starts {o.preferred_start}")
else:
    st.warning("Fill in owner info above to get started.")
    st.stop()   # nothing below makes sense without an owner

# ─────────────────────────────────────────────
# Section 2 — Add a pet
# ─────────────────────────────────────────────

st.divider()
st.header("2 · Add a Pet")

with st.form("pet_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pet_name = st.text_input("Pet name", value="Biscuit")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        breed = st.text_input("Breed (optional)", value="")
    with col4:
        age = st.number_input("Age", min_value=0, max_value=30, value=0)

    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet:
    owner = st.session_state.owner
    existing_names = [p.name.lower() for p in owner.get_pets()]
    if pet_name.lower() in existing_names:
        st.warning(f"A pet named **{pet_name}** is already registered.")
    else:
        new_pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
        owner.add_pet(new_pet)
        # Create a Scheduler for this pet immediately
        st.session_state.schedulers[pet_name] = Scheduler(owner=owner, pet=new_pet)
        st.success(f"🐾 **{pet_name}** the {species} added!")

# Show registered pets
pets = st.session_state.owner.get_pets()
if pets:
    st.write("**Registered pets:**", ", ".join(p.name for p in pets))
else:
    st.info("No pets yet — add one above.")

# ─────────────────────────────────────────────
# Section 3 — Add tasks
# ─────────────────────────────────────────────

st.divider()
st.header("3 · Add Tasks")

if not pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_pet = st.selectbox("Pet", [p.name for p in pets])
        with col2:
            task_title = st.text_input("Task title", value="Morning walk")

        col3, col4, col5 = st.columns(3)
        with col3:
            duration = st.number_input(
                "Duration (min)", min_value=1, max_value=240, value=30
            )
        with col4:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with col5:
            recurrence = st.selectbox("Recurrence", ["daily", "weekly", "as_needed"])

        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        scheduler = st.session_state.schedulers.get(selected_pet)
        if scheduler is None:
            st.error(f"No scheduler found for {selected_pet}. Try re-adding the pet.")
        else:
            try:
                scheduler.add_task(
                    Task(
                        title=task_title,
                        duration_minutes=int(duration),
                        priority=priority,
                        recurrence=recurrence,
                    )
                )
                st.success(f"✅ Added **{task_title}** to {selected_pet}.")
            except ValueError as e:
                st.warning(str(e))

    # Show current tasks per pet
    for pet in pets:
        tasks = pet.get_tasks()
        if tasks:
            with st.expander(f"🐾 {pet.name}'s tasks ({len(tasks)})", expanded=False):
                st.table(
                    [
                        {
                            "Task": t.title,
                            "Duration (min)": t.duration_minutes,
                            "Priority": t.priority,
                            "Recurrence": t.recurrence,
                        }
                        for t in tasks
                    ]
                )

# ─────────────────────────────────────────────
# Section 4 — Generate schedule
# ─────────────────────────────────────────────

st.divider()
st.header("4 · Generate Schedule")

if not pets:
    st.info("Add a pet and some tasks first.")
else:
    if st.button("🗓️ Build Today's Schedule", type="primary"):
        any_tasks = any(len(p.get_tasks()) > 0 for p in pets)
        if not any_tasks:
            st.warning("No tasks found. Add tasks in Step 3 first.")
        else:
            for pet in pets:
                scheduler = st.session_state.schedulers.get(pet.name)
                if scheduler is None or len(pet.get_tasks()) == 0:
                    continue

                scheduler.build_plan()

                st.subheader(f"🐾 {pet.name}")

                # Schedule table
                if scheduler.plan:
                    st.table(
                        [
                            {
                                "Time": t.scheduled_time,
                                "Task": t.title,
                                "Duration (min)": t.duration_minutes,
                                "Priority": t.priority,
                            }
                            for t in scheduler.plan
                        ]
                    )
                    used = sum(t.duration_minutes for t in scheduler.plan)
                    st.caption(
                        f"Time used: {used} / "
                        f"{st.session_state.owner.available_minutes} min"
                    )
                else:
                    st.info("No tasks fit the time budget.")

                # Explanation
                with st.expander("Why was this plan chosen?"):
                    st.text(scheduler.explain_plan())