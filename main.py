from monarch import Monarch

monarch_controller=Monarch()
print("\n------------------------------")

task_1="Write a short, exciting description for a new sci-fi movie about AI agents."
task_2="Create a python script to print number from 1 to 10."

print(f"\n [USER COMMAND]: {task_1}")
result_1=monarch_controller.assign_task(task_1)
if result_1:
    print("\n--- Monarch's Final Report ---")
    print(result_1)
    print("--------------------------------")

print(f"\n [USER COMMAND]: {task_2}")
result_2=monarch_controller.assign_task(task_2)
if result_2:
    print("\n--- Monarch's Final Report ---")
    print(result_2)
    print("--------------------------------")
