
import streamlit as st

from database import (
    add_subject,
    get_subjects,
    update_subject,
    delete_subject
)


def confirm_deletion(subject_id, code, name):

    st.warning(
        f"Are you sure you want to delete **{code} - {name}**?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Yes, Delete",
            type="primary",
            key=f"modal_del_{subject_id}"
        ):
            success, message = delete_subject(subject_id)

            if success:
                st.session_state["toast_message"] = (
                    "info",
                    "Subject deleted successfully!"
                )
            else:
                st.session_state["toast_message"] = (
                    "error",
                    message
                )

            st.rerun()

    with col2:
        if st.button(
            "Cancel",
            key=f"modal_cancel_{subject_id}"
        ):
            st.rerun()


@st.dialog("Confirm Deletion")
def deletion_dialog(subject_id, code, name):
    confirm_deletion(subject_id, code, name)


def show():

    # Persistent Notifications
    if "toast_message" in st.session_state:

        msg_type, msg_text = st.session_state["toast_message"]

        if msg_type == "success":
            st.success(msg_text)

        elif msg_type == "error":
            st.error(msg_text)

        elif msg_type == "warning":
            st.warning(msg_text)

        elif msg_type == "info":
            st.info(msg_text)

        del st.session_state["toast_message"]


    st.header("📖 Subject Management")


    # Add Subject
    st.subheader("➕ Add a Subject")

    with st.form("add_subject_form", clear_on_submit=True):

        code = st.text_input(
            "Subject Code",
            placeholder="e.g. CSCI101"
        )

        name = st.text_input(
            "Subject Name",
            placeholder="e.g. Introduction to Computer Science"
        )

        submitted = st.form_submit_button("Add Subject")

        if submitted:

            success, message = add_subject(code, name)

            if success:
                st.session_state["toast_message"] = (
                    "success",
                    message
                )
            else:
                st.session_state["toast_message"] = (
                    "warning",
                    message
                )

            st.rerun()


    st.divider()


    # Display Subjects
    st.subheader("📚 My Subjects")

    subjects = get_subjects()

    if subjects:

        for subject_id, code, name in subjects:

            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

            with col1:
                st.write(f"📘 **{code}** - {name}")

            with col2:

                with st.expander("✏️ Edit"):

                    with st.form(key=f"edit_form_{subject_id}"):

                        updated_code = st.text_input(
                            "Edit Code",
                            value=code
                        )

                        updated_name = st.text_input(
                            "Edit Name",
                            value=name
                        )

                        save_button = st.form_submit_button(
                            "Save Changes"
                        )

                        if save_button:

                            success, message = update_subject(
                                subject_id,
                                updated_code,
                                updated_name
                            )

                            if success:
                                st.session_state["toast_message"] = (
                                    "success",
                                    message
                                )
                            else:
                                st.session_state["toast_message"] = (
                                    "error",
                                    message
                                )

                            st.rerun()


            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"del_btn_{subject_id}"
                ):

                    deletion_dialog(
                        subject_id,
                        code,
                        name
                    )

    else:

        st.info(
            "No subjects yet. Add your first subject above!"
        )
