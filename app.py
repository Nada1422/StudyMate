import streamlit as st

st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyMate")
st.subheader("Your personal study planner")

st.write(
    "Welcome! Let's organize your studies "
    "and track your progress."
)

subject = st.text_input("Enter a subject")

if st.button("Add Subject"):
    if subject.strip():
        st.success(f"{subject} added successfully!")
    else:
        st.warning("Please enter a subject.")
