from agent import ShadowAgent

class Monarch:
    """
    The central commander. It receives tasks, creates agents,
    and delegates the work.
    """
    def __init__(self):
        self.army={}
        self.agent_counter=0
        print("Monarch System Initialized. Awaiting commands.")

    def assign_task(self, user_prompt):
        """
        The core logic of the Monarch. It analyzes the prompt and
        deploy the correct typer of agent.
        """
        if "summarize" in user_prompt.lower() or "write" in user_prompt.lower() or "describe" in user_prompt.lower():
            specialty="Copywriter"
        elif "code" in user_prompt.lower() or "script" in user_prompt.lower() or "function" in user_prompt.lower():
            specialty="Developer"
        else:
            specialty="Generalist"

        self.agent_counter+=1
        agent_id=f"{specialty[0]}-{self.agent_counter:03d}"
        print(f"Monarch Decision: A '{specialty}' is required. Summoning agent {agent_id}.")

        shadow_agent=ShadowAgent(
            agent_id=agent_id,
            rank="F",
            specialty=specialty
        )
        self.army[agent_id]=shadow_agent

        result=shadow_agent.perform_task(user_prompt)
        return result