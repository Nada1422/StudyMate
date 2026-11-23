
import streamlit as st
from database import init_db
import subject_management

st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="wide"
)

init_db()

st.title("📚 StudyMate")
st.subheader("Your personal study planner")

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Subject Management"]
)

if page == "Home":
    st.write(
        "Organize your subjects and track your progress."
    )

elif page == "Subject Management":
    subject_management.show()
