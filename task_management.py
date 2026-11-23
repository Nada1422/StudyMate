
import streamlit as st

from datetime import date

from database import (
    add_task,
    get_tasks,
    update_task,
    delete_task,
    get_subjects
)


def show():

    st.header("📝 Task Management")

    subjects = get_subjects()

    if not subjects:

        st.warning(
            "Please add a subject first before creating tasks."
        )

        return

    # =========================
    # ADD TASK
    # =========================

    st.subheader("➕ Add a Task")

    with st.form("add_task_form", clear_on_submit=True):

        title = st.text_input(
            "Task Title",
            placeholder="e.g. Solve Assignment 1"
        )

        description = st.text_area(
            "Description",
            placeholder="Enter task details..."
        )

        selected_subject = st.selectbox(
            "Subject",
            subjects,
            format_func=lambda s: f"{s[1]} - {s[2]}"
        )

        deadline = st.date_input(
            "Deadline",
            min_value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        submitted = st.form_submit_button("Add Task")

        if submitted:

            success, message = add_task(
                title,
                description,
                selected_subject[0],
                deadline.isoformat(),
                priority
            )

            if success:

                st.success(message)
                st.rerun()

            else:

                st.warning(message)

    st.divider()

    # =========================
    # DISPLAY TASKS
    # =========================

    st.subheader("📋 My Tasks")

    tasks = get_tasks()

    if not tasks:

        st.info(
            "No tasks yet. Add your first task above!"
        )

        return

    for task in tasks:

        (
            task_id,
            title,
            description,
            subject_id,
            subject_code,
            subject_name,
            deadline,
            priority,
            status
        ) = task

        task_deadline = date.fromisoformat(deadline)

        with st.expander(f"📌 {title}"):

            st.write(
                f"**Subject:** {subject_code} - {subject_name}"
            )

            st.write(f"**Deadline:** {deadline}")

            st.write(f"**Priority:** {priority}")

            st.write(f"**Status:** {status}")

            if description:

                st.write(f"**Description:** {description}")

            # Deadline Notifications

            if status != "Completed":

                if task_deadline < date.today():

                    st.error("⚠️ Overdue Task!")

                elif task_deadline == date.today():

                    st.warning("⏰ Due Today!")

                else:

                    days_left = (
                        task_deadline - date.today()
                    ).days

                    if days_left <= 3:

                        st.warning(
                            f"⏳ Due in {days_left} days!"
                        )

            st.divider()

            # =========================
            # EDIT TASK
            # =========================

            st.write("✏️ **Edit Task**")

            with st.form(key=f"edit_task_{task_id}"):

                updated_title = st.text_input(
                    "Task Title",
                    value=title,
                    key=f"title_{task_id}"
                )

                updated_description = st.text_area(
                    "Description",
                    value=description or "",
                    key=f"description_{task_id}"
                )

                subject_ids = [
                    s[0] for s in subjects
                ]

                current_index = subject_ids.index(subject_id)

                updated_subject = st.selectbox(
                    "Subject",
                    subjects,
                    index=current_index,
                    format_func=lambda s: f"{s[1]} - {s[2]}",
                    key=f"subject_{task_id}"
                )

                updated_deadline = st.date_input(
                    "Deadline",
                    value=task_deadline,
                    key=f"deadline_{task_id}"
                )

                updated_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High"],
                    index=[
                        "Low",
                        "Medium",
                        "High"
                    ].index(priority),
                    key=f"priority_{task_id}"
                )

                updated_status = st.selectbox(
                    "Status",
                    [
                        "Pending",
                        "In Progress",
                        "Completed"
                    ],
                    index=[
                        "Pending",
                        "In Progress",
                        "Completed"
                    ].index(status),
                    key=f"status_{task_id}"
                )

                save = st.form_submit_button(
                    "Save Changes"
                )

                if save:

                    success, message = update_task(
                        task_id,
                        updated_title,
                        updated_description,
                        updated_subject[0],
                        updated_deadline.isoformat(),
                        updated_priority,
                        updated_status
                    )

                    if success:

                        st.success(message)

                    else:

                        st.error(message)

                    st.rerun()

            st.divider()

            # =========================
            # DELETE TASK
            # =========================

            if st.button(
                "🗑️ Delete Task",
                key=f"delete_task_{task_id}",
                type="secondary"
            ):

                success, message = delete_task(task_id)

                if success:

                    st.success(message)

                else:

                    st.error(message)

                st.rerun()