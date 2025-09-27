# main.py
from monarch import Monarch

monarch_controller = Monarch()
print("\n" + "="*50)

# --- Test a job that requires the Code Interpreter tool ---
coder_task = "Create a Python function that calculates the factorial of a number and write a test case to prove it works for the number 5."

print(f"\n[USER JOB REQUIRING CODE INTERPRETER]: {coder_task}")
coder_report, _ = monarch_controller.execute_job(coder_task)

if coder_report:
    print("\n--- CODER GUILD DELIVERABLE ---")
    print(coder_report)
else:
    print("Coder Guild job could not be completed.")

print("\n" + "="*50)
monarch_controller.save_army()