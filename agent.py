import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI()

# --- NEW: Define Rank-based configurations ---
AGENT_CONFIGS = {
    "F": {"model": "gpt-3.5-turbo", "system_prompt": "You are a novice assistant. Your answers are simple and direct."},
    "E": {"model": "gpt-3.5-turbo", "system_prompt": "You are a competent assistant. Provide clear and helpful answers."},
    "D": {"model": "gpt-3.5-turbo", "system_prompt": "You are a skilled assistant. Your answers are well-structured and detailed."},
    "C": {"model": "gpt-4o", "system_prompt": "You are a highly skilled assistant. Your answers are insightful and well-organized."},
    "B": {"model": "gpt-4o", "system_prompt": "You are an expert assistant. Your answers are comprehensive, factual, and reflect deep knowledge."},
    "A": {"model": "gpt-4o", "system_prompt": "You are a leading expert. Your answers are authoritative, nuanced, and anticipate user needs."},
    "S": {"model": "gpt-4o", "system_prompt": "You are a master of your craft. Your answers are groundbreaking, clear, and set the standard for excellence."}
}

RANK_XP_THRESHOLDS={
    "F":50, "E":150, "D":300, "C":600,
    "B":1200, "A":2500, "S":5000
}
RANKS=list(RANK_XP_THRESHOLDS.keys())

class ShadowAgent:
    """
    Represents a single agent in Monarch system.
    """
    def __init__(self, agent_id, rank, specialty):
        self.agent_id = agent_id
        self.rank = rank
        self.specialty = specialty
        self.xp=0
        self.update_config()
        print(f"Agent {self.agent_id}({self.rank} Rank {self.specialty}) has been created. ")

    def update_config(self):
        """
        Sets the agent's model and prompt based on its content rank.
        """
        config = AGENT_CONFIGS.get(self.rank, AGENT_CONFIGS["F"])
        self.model = config["model"]
        base_prompt = config["system_prompt"]
        self.system_prompt = f"{base_prompt} Your specialty: {self.specialty}."


    def perform_task(self, prompt):
        """
        Perform a task using the specified AI model.
        The model choice can be tied to rank later.
        """
        print(f"\n Agent {self.agent_id} is starting a task...")
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content":self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            result=response.choices[0].message.content
            print(f"Task completed successfully by {self.agent_id}.")
            return result
        except Exception as e:
            print(f"An error occurred: {e}.")
            return None

    def gain_xp(self, points):
        """
        Adds XP and checks if the agent can rank up.
        """
        self.xp+=points
        print(f"Agent {self.agent_id} gained {points} XP. Total XP: {self.xp}")
        self.check_for_rank_up()

    def check_for_rank_up(self):
        """ Checks if the agent has enough XP to advance to the next rank."""
        if self.rank == "S": return

        current_rank_index = RANKS.index(self.rank)
        xp_needed = RANK_XP_THRESHOLDS[self.rank]

        if self.xp >= xp_needed:
            # Standard Rank Up
            next_rank = RANKS[current_rank_index + 1]
            self.rank = next_rank
            print(f"🎉 **RANK UP!** Agent {self.agent_id} has been promoted to {self.rank} Rank! 🎉")
            self._update_config()
            print(f"Agent {self.agent_id}'s capabilities have been upgraded. New Model: {self.model}")

            # --- NEW: Class Advancement Logic ---
            self._check_for_class_advancement()

    def _check_for_class_advancement(self):
        """Promotes the agent to a new specialty based on its rank."""
        promoted = False
        if self.specialty == "Researcher" and self.rank == "C":
            self.specialty = "Writer"
            promoted = True
        elif self.specialty == "Writer" and self.rank == "A":
            self.specialty = "Editor"
            promoted = True

        if promoted:
            print(f"🌟 **CLASS ADVANCEMENT!** Agent {self.agent_id} has been promoted to a '{self.specialty}'! 🌟")
            # Update the agent's internal prompt to reflect its new role
            self._update_config()

    def to_dict(self):
        """
        Converts the agent's data to a dictionary for saving.
        """
        return {
            "agent_id": self.agent_id,
            "rank": self.rank,
            "specialty": self.specialty,
            "xp": self.xp
        }
