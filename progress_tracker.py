def calculate_progress(tasks):
    completed_tasks = 0

    for task in tasks:
        if task["status"] == "Completed":
            completed_tasks += 1

    total_tasks = len(tasks)

    if total_tasks == 0:
        return 0

    progress = (completed_tasks / total_tasks) * 100
    return progress


tasks = []

number = int(input("Enter number of tasks: "))

for i in range(number):
    print("\nTask", i + 1)

    name = input("Enter task name: ")
    status = input("Enter status (Completed/Not Completed): ")

    tasks.append({
        "name": name,
        "status": status
    })


print("\nStudy Progress")
print("----------------")

for task in tasks:
    print(task["name"], "-", task["status"])

progress = calculate_progress(tasks)

print("\nCompleted Progress:", progress, "%")
