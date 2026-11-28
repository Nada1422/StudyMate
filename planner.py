def sort_tasks(tasks):
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    tasks.sort(
        key=lambda task: priority_order[task["priority"].lower()]
    )

    return tasks


def create_schedule(tasks, available_hours):
    tasks = sort_tasks(tasks)
    schedule = []

    for task in tasks:
        if available_hours <= 0:
            break

        study_hours = min(task["hours"], available_hours)

        schedule.append({
            "name": task["name"],
            "subject": task["subject"],
            "hours": study_hours
        })

        available_hours -= study_hours

    return schedule


def run_cli():
    # Get number of tasks
    while True:
        try:
            number = int(input("How many tasks do you have? "))

            if number > 0:
                break
            else:
                print("Please enter at least one task.")

        except ValueError:
            print("Please enter a valid whole number.")

    # Get task information
    tasks = []

    for i in range(number):
        print("\nTask", i + 1)

        while True:
            name = input("Enter task name: ").strip()

            if name:
                break
            print("Task name cannot be empty.")

        while True:
            subject = input("Enter subject: ").strip()

            if subject:
                break
            print("Subject cannot be empty.")

        while True:
            priority = input(
                "Enter priority (High/Medium/Low): "
            ).strip().capitalize()

            if priority in ["High", "Medium", "Low"]:
                break
            print("Invalid priority! Enter High, Medium, or Low.")

        while True:
            try:
                hours = float(input("Enter required study hours: "))

                if hours > 0:
                    break
                print("Hours must be greater than zero.")

            except ValueError:
                print("Please enter a valid number.")

        tasks.append({
            "name": name,
            "subject": subject,
            "priority": priority,
            "hours": hours
        })

    # Get available study hours
    while True:
        try:
            available_hours = float(
                input("\nHow many hours can you study today? ")
            )

            if available_hours > 0:
                break
            print("Available hours must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")

    # Create and display schedule
    schedule = create_schedule(tasks, available_hours)

    print("\nYour Study Schedule:")
    print("--------------------")

    for task in schedule:
        print(
            task["name"],
            "-",
            task["subject"],
            "-",
            task["hours"],
            "hours"
        )

    print("\nSchedule created successfully!")


if __name__ == "__main__":
    run_cli()