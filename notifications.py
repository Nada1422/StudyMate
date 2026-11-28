from datetime import date, datetime, time
from database import get_tasks


def _parse_deadline_dt(deadline_val):
    if isinstance(deadline_val, datetime):
        return deadline_val
    if isinstance(deadline_val, date):
        return datetime.combine(deadline_val, time(23, 59))

    text = str(deadline_val).strip()
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        try:
            d = date.fromisoformat(text[:10])
            return datetime.combine(d, time(23, 59))
        except ValueError:
            return None


def get_notifications(days_ahead=3, today=None):
    if days_ahead < 0:
        raise ValueError("days_ahead cannot be negative")

    if today is None:
        now = datetime.now()
    elif isinstance(today, datetime):
        now = today
    elif isinstance(today, date):
        now = datetime.combine(today, time(0, 0))
    else:
        now = datetime.now()

    current_date = now.date()
    notifications = []

    for task in get_tasks():
        task_id = task[0]
        title = task[1]
        subject = task[4]
        deadline = task[6]
        status = task[8]

        if status == "Completed":
            continue

        due_dt = _parse_deadline_dt(deadline)
        if due_dt is None:
            continue

        days_left = (due_dt.date() - current_date).days
        hours_left = (due_dt - now).total_seconds() / 3600

        if due_dt < now:
            alert_type = "Overdue"
            message = f"{title} is overdue!"
        elif due_dt.date() == current_date:
            alert_type = "Due Today"
            message = f"{title} is due today at {due_dt.strftime('%H:%M')}!"
        elif days_left <= days_ahead:
            alert_type = "Upcoming"
            message = f"{title} is due in {days_left} days ({due_dt.strftime('%Y-%m-%d %H:%M')})."
        else:
            continue

        notifications.append({
            "task_id": task_id,
            "title": title,
            "subject": subject,
            "deadline": due_dt.strftime("%Y-%m-%d %H:%M"),
            "type": alert_type,
            "message": message,
            "days_left": days_left,
            "hours_left": round(hours_left, 1),
        })

    notifications.sort(key=lambda item: item["hours_left"])
    return notifications