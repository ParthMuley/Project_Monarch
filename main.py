from monarch import Monarch

monarch_controller=Monarch()
print("\n------------------------------")

tasks = [
    "Write a short, exciting description for a new sci-fi movie.",
    "Summarize the plot of 'The Matrix' in two sentences.",
    "Describe the benefits of drinking water.",
    "Draft a tweet about a new tech product launch.",
]

for i, task in enumerate(tasks, 1):
    print(f"\n[USER COMMAND #{i}]: {task}")
    result = monarch_controller.assign_task(task)
    if result:
        print("\n--- Monarch's Report ---")
        print(result)
        print("------------------------")

# --- ADD THIS LINE AT THE VERY END ---
monarch_controller.save_army()