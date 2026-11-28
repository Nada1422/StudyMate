from datetime import date, datetime
from database import get_tasks


def get_notifications(days_ahead=3, today=None):
    if days_ahead < 0:
        raise ValueError("days_ahead cannot be negative")

    if today is None:
        today = date.today()
    elif isinstance(today, datetime):
        today = today.date()

    notifications = []

    for task in get_tasks():
        task_id = task[0]
        title = task[1]
        subject = task[4]
        deadline = task[6]
        status = task[8]

        if status == "Completed":
            continue

        try:
            due_date = date.fromisoformat(str(deadline)[:10])
        except ValueError:
            continue

        days_left = (due_date - today).days

        if days_left < 0:
            alert_type = "Overdue"
            message = f"{title} is overdue!"
        elif days_left == 0:
            alert_type = "Due Today"
            message = f"{title} is due today!"
        elif days_left <= days_ahead:
            alert_type = "Upcoming"
            message = f"{title} is due in {days_left} days."
        else:
            continue

        notifications.append({
            "task_id": task_id,
            "title": title,
            "subject": subject,
            "deadline": deadline,
            "type": alert_type,
            "message": message,
            "days_left": days_left,
        })

    notifications.sort(key=lambda item: item["days_left"])
    return notifications
