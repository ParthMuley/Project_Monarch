# monarch.py
import json
from logging import exception

from agent import ShadowAgent


class Monarch:
    def __init__(self, army_file="army.json"):
        self.army = {}
        self.army_file = army_file
        self.load_army()
        print(f"Monarch System Initialized. Managing {len(self.army)} army.")

    def save_army(self):
        """
        Saves the current state of the army to the JSON file.
        """
        print(f"Monarch : Saving the state of {len(self.army)} agents to {self.army_file}.")
        army_data={agent_id:agent.to_dict() for agent_id, agent in self.army.items()}
        with open(self.army_file, "w") as f:
            json.dump(army_data, f, indent=4)
        print("Save Complete.")

    def load_army(self):
        """
        Loads the army srate from the JSON file if it exists.
        """
        try:
            with open(self.army_file, "r") as f:
                army_data = json.load(f)
                for agent_id, agent_info in army_data.items():
                    agent = ShadowAgent(
                        agent_id=agent_info["agent_id"],
                        rank=agent_info['rank'],
                        specialty=agent_info['specialty']
                    )
                    agent.xp = agent_info['xp']
                    self.army[agent_id] = agent
            print(f"Successfully Loaded {len(self.army)} agents from {self.army_file}.")
        except FileNotFoundError:
            print("No existing army file found. Starting with a new army.")
        except Exception as e:
            print(f"Could not load army file. Starting fresh. Error: {e}")

    def determine_specialty(self, user_prompt):
        """Helper function to decide the specialty."""
        prompt = user_prompt.lower()
        if "summarize" in prompt or "write" in prompt or "describe" in prompt:
            return "Copywriter"
        if "code" in prompt or "script" in prompt or "function" in prompt:
            return "Developer"
        return "Generalist"

    def find_available_agent(self, specialty):
        """Finds an existing agent of a specific specialty."""
        for agent in self.army.values():
            if agent.specialty == specialty:
                return agent
        return None

    def assign_task(self, user_prompt):
        specialty = self.determine_specialty(user_prompt)
        agent_to_assign = self.find_available_agent(specialty)
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