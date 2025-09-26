# main.py
from dotenv import load_dotenv
from monarch import Monarch

load_dotenv(override=True)

monarch_controller = Monarch()
print("\n" + "="*50)

# --- Define a single, complex, multi-guild prompt ---
master_prompt = "Generate a technical report on the performance of a Python function that calculates Fibonacci numbers, and you must include the function's complete code in the report."

print(f"\n[USER'S AUTONOMOUS JOB]: {master_prompt}")

# --- Give the Monarch the high-level task ---
# It will now create the plan AND execute it.
final_artifacts, job_history = monarch_controller.execute_complex_job(master_prompt)

print("\n--------------------------")
if final_artifacts:
    print("\n--- MONARCH'S FINAL DELIVERABLE (AUTONOMOUSLY GENERATED) ---")
    final_report = f"## Technical Report\n\n{final_artifacts.get('report', '')}\n\n## Appendix: Source Code\n\n```python\n{final_artifacts.get('code', '')}\n```"
    print(final_report)
else:
    print("The collaborative job could not be completed.")

print("\n" + "="*50)

monarch_controller.save_army()