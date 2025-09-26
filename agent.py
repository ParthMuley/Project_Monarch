import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI()

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
        print(f"Agent {self.agent_id}({self.rank} Rank {self.specialty}) has been created. ")

    def perform_task(self, prompt, model="gpt-3.5-turbo"):
        """
        Perform a task using the specified AI model.
        The model choice can be tied to rank later.
        """
        print(f"\n Agent {self.agent_id} is starting a task...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant with the specialty: {self.specialty}."},
                    {"role": "user", "content": prompt}
                ]
            )
            result=response.choices[0].message.content
            print(f"Task completed successfully.")
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
        self._check_for_rank_up()

    def _check_for_rank_up(self):
        """ Checks if the agent has enough XP to advance to the next rank."""
        if self.rank=="S":
            return
        current_rank_index=RANKS.index(self.rank)
        xp_needed=RANK_XP_THRESHOLDS[self.rank]

        if self.xp>=xp_needed:
            next_rank=RANKS[current_rank_index+1]
            self.rank=next_rank
            print(f"🎉 **RANK UP!** Agent {self.agent_id} has been promoted to {self.rank} Rank! 🎉")

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
