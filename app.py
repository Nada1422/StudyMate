
import streamlit as st

from database import init_db, add_subject, get_subjects

st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="wide"
)

init_db()

st.title("📚 StudyMate")
st.subheader("Your personal study planner")

st.write("Organize your subjects and track your progress.")

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
