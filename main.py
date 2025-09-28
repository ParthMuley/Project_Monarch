# main.py
from monarch import Monarch

monarch_controller = Monarch()
print("\n" + "="*50)

# --- Define a job that requires at least a C-Rank Writer ---
writer_task = "Write a professional summary of the plot of the movie 'Inception'."

print(f"\n[USER JOB]: {writer_task}")
final_report, _ = monarch_controller.execute_job(writer_task)

if final_report:
    print("\n--- WRITER GUILD DELIVERABLE ---")
    print(final_report)
else:
    print("Writer Guild job could not be completed.")

print("\n" + "="*50)
monarch_controller.save_army()