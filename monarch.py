# monarch.py
import json
from logging import exception
from Job import Job

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

    def get_agent(self, specialty, min_rank="F"):
        """Finds an available agent or creates one if none exist."""
        # This is a more advanced find logic, looking for best available rank
        best_agent = None
        for agent in self.army.values():
            if agent.specialty == specialty and agent.rank >= min_rank:
                if best_agent is None or agent.rank > best_agent.rank:
                    best_agent = agent

        if best_agent:
            print(f"Monarch: Found available agent {best_agent.agent_id} for the job.")
            return best_agent
        else:
            # If no suitable agent is found, create a new one
            agent_id = f"{specialty[0]}-{len(self.army) + 1:03d}"
            print(f"Monarch: No '{specialty}' of rank {min_rank}+. Summoning new agent {agent_id}.")
            new_agent = ShadowAgent(agent_id=agent_id, rank=min_rank, specialty=specialty)
            self.army[agent_id] = new_agent
            return new_agent

        # --- NEW ORCHESTRATION METHOD ---

    def execute_job(self, user_request):
        """Manages a multi-step job using a hierarchy of agents."""
        current_job = Job(user_request)
        current_job.status = "IN_PROGRESS"

        try:
            # Step 1: Outlining by a Researcher (Rank F+)
            outliner = self.get_agent("Researcher", "F")
            outline_prompt = f"Create a concise, bulleted outline for a report on the following topic: {user_request}"
            outline = outliner.perform_task(outline_prompt)
            if not outline: raise Exception("Outlining failed.")
            current_job.artifacts['outline'] = outline
            current_job.add_history(outliner.agent_id, "Generated Outline", outline)
            outliner.gain_xp(10)

            # Step 2: Drafting by a Writer (Rank C+)
            writer = self.get_agent("Writer", "C")
            draft_prompt = f"Using the following outline, write a detailed draft of the report. \n\nOUTLINE:\n{outline}"
            draft = writer.perform_task(draft_prompt)
            if not draft: raise Exception("Drafting failed.")
            current_job.artifacts['draft'] = draft
            current_job.add_history(writer.agent_id, "Wrote Draft", draft)
            writer.gain_xp(25)  # More complex tasks grant more XP

            # Step 3: Editing by an Editor (Rank A+)
            editor = self.get_agent("Editor", "A")
            edit_prompt = f"Review the following draft for clarity, accuracy, and style. Polish it into a final report. \n\nDRAFT:\n{draft}"
            final_report = editor.perform_task(edit_prompt)
            if not final_report: raise Exception("Editing failed.")
            current_job.artifacts['final_report'] = final_report
            current_job.add_history(editor.agent_id, "Finalized Report", final_report)
            editor.gain_xp(50)

            current_job.status = "COMPLETED"
            print(f"\nJob {current_job.id} completed successfully!")
            return final_report, current_job.history

        except Exception as e:
            current_job.status = "FAILED"
            print(f"Job {current_job.id} failed. Error: {e}")
            return None, current_job.history