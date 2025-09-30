# agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import AVAILABLE_TOOLS
from memory import recall
import json
import re

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
        self.update_config()
        print(f"Agent {self.agent_id} ({self.specialty}) has been instantiated.")

    def update_config(self):
        """Sets the agent's prompt based on its guild configuration."""
        self.system_prompt = self.guild_config["prompts"].get(self.specialty, "You are a helpful assistant.")

    def perform_task(self, prompt):
        """The agent's reasoning loop, with robust JSON parsing for tool decisions."""
        print(f"\nAgent {self.agent_id} ({self.rank} Rank) is analyzing the task: '{prompt[:50]}...'")

        tool_used_name = None
        recalled_memories = recall(query_texts=prompt)
        memory_context = ""
        if recalled_memories:
            memory_context = "I found this in my memory from a similar past job...\n---\n" + "\n\n".join(
                recalled_memories) + "\n---"
            print(f"Agent {self.agent_id} recalled relevant memories.")

        tool_decision_prompt = f"""
        {memory_context}
        You have access to the following tools: {list(AVAILABLE_TOOLS.keys())}.
        Based on the user's request, should you use a tool?
        If yes, respond with ONLY the JSON format: {{"tool_name": "name", "tool_input": "input for the tool"}}
        If no, respond with "NO_TOOL".
        User Request: "{prompt}"
        """

        try:
            decision_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a reasoning engine that decides which tool to use."},
                          {"role": "user", "content": tool_decision_prompt}]
            ).choices[0].message.content

            # --- NEW: Robust JSON Extraction Logic ---
            json_match = re.search(r'\{.*\}', decision_response, re.DOTALL)

            if "NO_TOOL" in decision_response or not json_match:
                print(f"Agent {self.agent_id} decided no tool is needed.")
                final_prompt = prompt
            else:
                tool_choice_str = json_match.group(0)
                tool_choice = json.loads(tool_choice_str)
                tool_name = tool_choice.get("tool_name")
                tool_input = tool_choice.get("tool_input")

                if tool_name in AVAILABLE_TOOLS:
                    print(f"Agent {self.agent_id} decided to use the '{tool_name}' tool.")
                    tool_used_name = tool_name
                    tool_function = AVAILABLE_TOOLS[tool_name]
                    tool_result = tool_function(tool_input)
                    final_prompt = f"The user's request was: '{prompt}'. I used the '{tool_name}' tool and got this result: '{tool_result}'. Now, provide a comprehensive final answer."
                else:
                    final_prompt = prompt
        except Exception as e:
            print(f"An error occurred during tool decision: {e}. Proceeding without a tool.")
            final_prompt = prompt

        # Final response generation
        final_response_text = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": final_prompt}]
        ).choices[0].message.content

        return {"response": final_response_text, "tool_used": tool_used_name}

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
        self.check_for_rank_up()

    def check_for_rank_up(self):
        if self.rank == "S": return

        # Check for promotions iteratively, in case of multiple rank-ups
        while self.rank != "S":
            current_rank_index = RANKS.index(self.rank)
            next_rank_index = current_rank_index + 1

            if next_rank_index >= len(RANKS): break  # Should not happen if rank is not S, but safe check

            next_rank = RANKS[next_rank_index]
            xp_needed = RANK_XP_THRESHOLDS.get(next_rank)

            if self.xp >= xp_needed:
                # If XP is sufficient for the NEXT rank, then promote
                previous_rank = self.rank
                self.rank = next_rank
                print(f"🎉 **RANK UP!** Agent {self.agent_id} has been promoted to {self.rank} Rank! 🎉")
                self.check_for_class_advancement(previous_rank)
                self.update_config()
            else:
                # If XP is not enough for the next rank, stop checking
                break

    def check_for_class_advancement(self):  # Argument removed
        """Promotes the agent based on its current, newly achieved rank."""
        for promotion in self.guild_config.get("career_path", []):
            # Check against the agent's NEW, current rank
            if promotion["from"] == self.specialty and self.rank == promotion["at_rank"]:
                self.specialty = promotion["to"]
                print(f"🌟 **CLASS ADVANCEMENT!** Agent {self.agent_id} has been promoted to a '{self.specialty}'! 🌟")
                break  # Important to stop after the first valid promotion

    def to_dict(self):
        return {"agent_id": self.agent_id, "rank": self.rank, "specialty": self.specialty, "xp": self.xp}