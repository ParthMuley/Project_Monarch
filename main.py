# main.py
from monarch import Monarch

# Initialize the Monarch. Since army.json is gone, it will start fresh.
monarch_controller = Monarch()
print("\n" + "="*50)

# --- Define a complex job that requires high-rank agents ---
complex_task = "Create a Python script for a basic command-line calculator that can add, subtract, multiply, and divide."

print(f"\n[USER JOB]: {complex_task}")

# --- Execute the job ---
final_product, job_history = monarch_controller.execute_job(complex_task)

print("\n--------------------------")
if final_product:
    print("\n--- MONARCH'S FINAL DELIVERABLE ---")
    print(final_product)
    print("\n--- JOB HISTORY ---")
    for entry in job_history:
        print(entry)
else:
    print("The job could not be completed.")


print("\n" + "="*50)

# Save the updated state of the army
monarch_controller.save_army()