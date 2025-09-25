import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client=OpenAI()

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
