# main.py
from monarch import Monarch

monarch_controller = Monarch()
print("\n" + "="*50)

# --- Test a job that requires a tool ---
# We'll use a simple, single-step job for this test.
# Make sure you have a D-Rank or higher "Researcher" agent.
# If not, run a few writer jobs first to level one up.
tool_task = "What is the latest news about NASA's Artemis program?"
print(f"\n[USER JOB REQUIRING A TOOL]: {tool_task}")

# For this test, let's just get the best researcher to do it.
researcher_agent = monarch_controller.get_agent("Researcher", monarch_controller.guilds["Writer"])
if researcher_agent:
    final_report = researcher_agent.perform_task(tool_task)
    if final_report:
        print("\n--- AGENT'S FINAL REPORT (WITH TOOL) ---")
        print(final_report)
else:
    print("No researcher agent found.")

print("\n" + "="*50)
monarch_controller.save_army()