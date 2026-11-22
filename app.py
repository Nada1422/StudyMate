import streamlit as st

from database import init_db, add_subject, get_subjects

st.set_page_config(page_title="StudyMate", page_icon="📚", layout="wide")
init_db()

st.title("📚 StudyMate")
st.subheader("Your personal study planner")

tab_subjects, tab_tasks, tab_planner, tab_analytics, tab_alerts = st.tabs(
    ["Subjects", "Tasks", "Study Planner", "Analytics", "Notifications"]
)

with tab_subjects:
    subject = st.text_input("Enter a subject")

    if st.button("Add Subject"):
        success, message = add_subject(subject)
        if success:
            st.success(message)
        else:
            st.warning(message)

    st.divider()
    st.subheader("📖 My Subjects")

    subjects = get_subjects()
    if subjects:
        for subject_id, subject_name in subjects:
            st.write(f"📘 {subject_name}")
    else:
        st.info("No subjects yet. Add your first subject above!")

with tab_tasks:
    st.info("Placeholder: task manager (Member 1)")

with tab_planner:
    st.info("Placeholder: study schedule (Member 2)")

with tab_analytics:
    st.info("Placeholder: charts and progress (Member 3)")

with tab_alerts:
    st.info("Placeholder: notifications (Member 4)")