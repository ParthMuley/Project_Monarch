# agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

RANK_XP_THRESHOLDS = {"F": 50, "E": 150, "D": 300, "C": 600, "B": 1200, "A": 2500, "S": 5000}
RANKS = list(RANK_XP_THRESHOLDS.keys())

class ShadowAgent:
    def __init__(self, agent_id, rank, specialty, guild_config):
        self.agent_id = agent_id
        self.rank = rank
        self.specialty = specialty
        self.xp = 0
        self.guild_config = guild_config
        self._update_config()
        print(f"Agent {self.agent_id} ({self.rank} Rank {self.specialty}) has been created.")

    def _update_config(self):
        """Sets the agent's prompt based on its guild configuration."""
        self.system_prompt = self.guild_config["prompts"].get(self.specialty, "You are a helpful assistant.")

    def perform_task(self, prompt):
        print(f"\nAgent {self.agent_id} ({self.rank} Rank, Specialty: {self.specialty}) is starting a text task...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred during text task: {e}")
            return None

    def create_image(self, prompt):
        print(f"\nAgent {self.agent_id} ({self.rank} Rank {self.specialty}) is creating an image...")
        try:
            response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", n=1)
            return response.data[0].url
        except Exception as e:
            print(f"An error occurred during image creation: {e}")
            return None

    def gain_xp(self, points):
        self.xp += points
        print(f"Agent {self.agent_id} gained {points} XP. Total XP: {self.xp}")
        self._check_for_rank_up()

    def _check_for_rank_up(self):
        if self.rank == "S": return
        if self.xp >= RANK_XP_THRESHOLDS.get(self.rank, float('inf')):
            previous_rank = self.rank  # Remember the rank the agent is leaving

            # 1. Promote Rank First
            current_rank_index = RANKS.index(self.rank)
            self.rank = RANKS[current_rank_index + 1]
            print(f"🎉 **RANK UP!** Agent {self.agent_id} has been promoted to {self.rank} Rank! 🎉")

            # 2. THEN, check if leaving the previous rank triggered a class advancement
            self._check_for_class_advancement(previous_rank)

            # 3. Finally, update the config with the new rank/specialty
            self._update_config()

    def _check_for_class_advancement(self, rank_they_are_leaving):
        """Promotes the agent based on the rank it just completed."""
        for promotion in self.guild_config.get("career_path", []):
            if promotion["from"] == self.specialty and rank_they_are_leaving == promotion["at_rank"]:
                self.specialty = promotion["to"]
                print(f"🌟 **CLASS ADVANCEMENT!** Agent {self.agent_id} has been promoted to a '{self.specialty}'! 🌟")
                # The _update_config call will happen once in _check_for_rank_up
                break

    def to_dict(self):
        return {"agent_id": self.agent_id, "rank": self.rank, "specialty": self.specialty, "xp": self.xp}