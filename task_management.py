import streamlit as st
from datetime import date, datetime, time

from database import (
    add_task,
    get_tasks,
    update_task,
    delete_task,
    get_subjects
)


def parse_deadline(deadline_str):
    text = str(deadline_str).strip()
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        parsed_date = date.fromisoformat(text[:10])
        return datetime.combine(parsed_date, time(23, 59))


def format_deadline(deadline_str):
    dt = parse_deadline(deadline_str)
    if "T" in str(deadline_str) or " " in str(deadline_str):
        return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime("%Y-%m-%d")


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

        col_date, col_time = st.columns(2)

        with col_date:
            deadline_date = st.date_input(
                "Deadline Date",
                min_value=date.today()
            )

        with col_time:
            deadline_time = st.time_input(
                "Deadline Time",
                value=time(23, 59)
            )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        submitted = st.form_submit_button("Add Task")

        if submitted:
            deadline_dt = datetime.combine(deadline_date, deadline_time)

            success, message = add_task(
                title,
                description,
                selected_subject[0],
                deadline_dt.isoformat(),
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

        task_deadline_dt = parse_deadline(deadline)
        now = datetime.now()

        with st.expander(f"📌 {title}"):
            st.write(
                f"**Subject:** {subject_code} - {subject_name}"
            )

            st.write(f"**Deadline:** {format_deadline(deadline)}")

            st.write(f"**Priority:** {priority}")

            st.write(f"**Status:** {status}")

            if description:
                st.write(f"**Description:** {description}")

            # Deadline Notifications

            if status != "Completed":
                if task_deadline_dt < now:
                    st.error("⚠️ Overdue Task!")
                elif task_deadline_dt.date() == now.date():
                    st.warning("⏰ Due Today!")
                else:
                    remaining_hours = (task_deadline_dt - now).total_seconds() / 3600
                    days_left = (task_deadline_dt.date() - now.date()).days

                    if remaining_hours <= 72 or days_left <= 3:
                        st.warning(
                            f"⏳ Due soon ({max(1, round(remaining_hours))} hours left)!"
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

                edit_col_date, edit_col_time = st.columns(2)

                with edit_col_date:
                    updated_date = st.date_input(
                        "Deadline Date",
                        value=task_deadline_dt.date(),
                        key=f"deadline_date_{task_id}"
                    )

                with edit_col_time:
                    updated_time = st.time_input(
                        "Deadline Time",
                        value=task_deadline_dt.time().replace(microsecond=0),
                        key=f"deadline_time_{task_id}"
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
                    updated_deadline_dt = datetime.combine(updated_date, updated_time)

                    success, message = update_task(
                        task_id,
                        updated_title,
                        updated_description,
                        updated_subject[0],
                        updated_deadline_dt.isoformat(),
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