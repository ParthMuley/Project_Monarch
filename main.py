from agent import ShadowAgent

writer_agent_001=ShadowAgent(agent_id="W-001", rank="F", specialty="CopyWriter")
task_prompt="Summarize the concept of photosynthesis in a single, simple paragraph "
result=writer_agent_001.perform_task(task_prompt)
if result:
    print("\n--- Agent's Final Output ---")
    print(result)
    print("------------------------------")