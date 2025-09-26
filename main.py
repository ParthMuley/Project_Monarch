# main.py
from monarch import Monarch

monarch_controller = Monarch()
print("\n--------------------------")

# Define a complex job for the Monarch
complex_task = "The impact of renewable energy on the global economy"

print(f"\n[USER'S COMPLEX JOB]: Create a report on '{complex_task}'")
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

# Don't forget to save the army's progress!
monarch_controller.save_army()