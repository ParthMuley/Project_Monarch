# main.py
from dotenv import load_dotenv
from monarch import Monarch

load_dotenv(override=True)

monarch_controller = Monarch()
print("\n" + "="*50)

# --- Define a job for the Writer's Guild ---
writer_task = "The rise and fall of the Mayan civilization"
print(f"\n[USER'S COMPLEX JOB]: Create a report on '{writer_task}'")
writer_product, writer_history = monarch_controller.execute_job(writer_task)

if writer_product:
    print("\n--- WRITER GUILD DELIVERABLE ---")
    print(writer_product)
else:
    print("\nWriter Guild job could not be completed.")

print("\n" + "="*50)

# --- Define a job for the Coder's Guild ---
coder_task = "Create a Python script that fetches the current weather for a given city using an online API."
print(f"\n[USER'S COMPLEX JOB]: {coder_task}")
coder_product, coder_history = monarch_controller.execute_job(coder_task)

if coder_product:
    print("\n--- CODER GUILD DELIVERABLE ---")
    print(coder_product)
else:
    print("\nCoder Guild job could not be completed.")

print("\n" + "="*50)

# Save the progress of all agents
monarch_controller.save_army()