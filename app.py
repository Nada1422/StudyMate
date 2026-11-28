import streamlit as st

from database import init_db, get_tasks
from notifications import get_notifications
from progress_tracker import calculate_progress
import subject_management
import task_management


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
    [
        "Home",
        "Subject Management",
        "Task Management"
    ]
)

if page == "Home":
    st.write("Organize your subjects and track your progress.")

    tasks = get_tasks()
    task_dicts = [{"status": row[8]} for row in tasks]
    progress = calculate_progress(task_dicts)

    st.metric("Overall Completion Progress", f"{progress:.1f}%")
    st.progress(min(max(progress / 100.0, 0.0), 1.0))

    st.divider()
    st.subheader("🔔 Deadline Alerts")

    alerts = get_notifications(days_ahead=3)
    if not alerts:
        st.info("No overdue or upcoming deadlines in the next 3 days.")
    else:
        for alert in alerts:
            label = f"**[{alert['subject']}]** {alert['message']} *(Deadline: {alert['deadline']})*"
            if alert["type"] == "Overdue":
                st.error(label)
            else:
                st.warning(label)

elif page == "Subject Management":
    subject_management.show()

elif page == "Task Management":
    task_management.show()