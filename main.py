# main.py
from monarch import Monarch

# Initialize the Monarch. It will load the army, guilds, and memory.
monarch_controller = Monarch()
print("\n" + "="*50)

# --- Define the job we will use for the memory test ---
memory_test_task = "Write a short Python script to ping a website and see if it's online."

print(f"\n[USER JOB]: {memory_test_task}")

# --- Execute the job ---
final_product, job_history = monarch_controller.execute_job(memory_test_task)

print("\n--------------------------")
if final_product:
    print("\n--- MONARCH'S FINAL DELIVERABLE ---")
    print(final_product)
else:
    print("The job could not be completed.")

print("\n" + "="*50)

# Save the updated state of the army
monarch_controller.save_army()