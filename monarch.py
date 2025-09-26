# monarch.py
from agent import ShadowAgent


class Monarch:
    def __init__(self):
        self.army = {}
        print("Monarch System Initialized. Managing a persistent army.")

    def _determine_specialty(self, user_prompt):
        """Helper function to decide the specialty."""
        prompt = user_prompt.lower()
        if "summarize" in prompt or "write" in prompt or "describe" in prompt:
            return "Copywriter"
        if "code" in prompt or "script" in prompt or "function" in prompt:
            return "Developer"
        return "Generalist"

    def _find_available_agent(self, specialty):
        """Finds an existing agent of a specific specialty."""
        for agent in self.army.values():
            if agent.specialty == specialty:
                return agent
        return None

    def assign_task(self, user_prompt):
        specialty = self._determine_specialty(user_prompt)

        # --- THIS IS THE NEW LOGIC ---
        agent_to_assign = self._find_available_agent(specialty)

        if not agent_to_assign:
            # If no agent is found, summon a new one and add it to the army
            agent_id = f"{specialty[0]}-{len(self.army) + 1:03d}"
            print(f"Monarch: No available '{specialty}'. Summoning new agent {agent_id}.")
            agent_to_assign = ShadowAgent(agent_id=agent_id, rank="F", specialty=specialty)
            self.army[agent_id] = agent_to_assign
        else:
            # If an agent is found, reuse it
            print(f"Monarch: Found available agent {agent_to_assign.agent_id}. Assigning task.")

        # Delegate the task and award XP on success
        result = agent_to_assign.perform_task(user_prompt)
        if result:
            agent_to_assign.gain_xp(15)  # Award 15 XP for a completed task

        return result