# monarch.py
import json
import re
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

    def determine_guild(self, user_prompt):
        """
        Determine the required GUILD  and starting specialty for a task.
        Acts as the high-level dispatcher.
        """
        prompt = user_prompt.lower()
        if any(keyword in prompt for keyword in ["code", "script", "methods", "program", "app"]):
            return "Coder"  # Starting role for the Coder Guild
        return "Writer"

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

    # --- THIS IS THE NEW TOP-LEVEL METHOD ---
    def execute_complex_job(self, user_request):
        """Decomposes a request and executes the generated plan."""
        print("Monarch: Accessing Planner to decompose the user's request...")

        # Step 1: Decompose the request into a plan using a Planner agent
        project_plan = self._decompose_request_into_plan(user_request)
        if not project_plan:
            print("Monarch: Failed to create a project plan. Aborting.")
            return None, None

        # Step 2: Execute the plan
        return self._execute_plan(user_request, project_plan)

    def _decompose_request_into_plan(self, user_request):
        """Uses a specialized S-Rank Planner agent to create a project plan."""
        try:
            planner_agent = self.get_agent("Planner", "S")
            raw_output = planner_agent.perform_task(user_request)

            # --- NEW: Robust JSON Extraction Logic ---
            print(f"DEBUG: Planner's raw output:\n---\n{raw_output}\n---")

            # Use regex to find a JSON list '[...]' or object '{...}'
            json_match = re.search(r'\[.*\]|\{.*\}', raw_output, re.DOTALL)

            if json_match:
                plan_str = json_match.group(0)
                print(f"DEBUG: Extracted JSON string:\n---\n{plan_str}\n---")
                project_plan = json.loads(plan_str)
                return project_plan
            else:
                print("Error: No valid JSON block found in the Planner's output.")
                return None
            # --- END OF NEW LOGIC ---

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from planner: {e}")
            return None
        except Exception as e:
            print(f"An error occurred during the planning phase: {e}")
            return None

    def _execute_plan(self, user_request, project_plan):
        """Executes a list of sub-tasks, replacing the old execute_job method."""
        current_job = Job(user_request)
        current_job.status = "IN_PROGRESS"
        print(f"Monarch: Plan created with {len(project_plan)} steps. Starting execution.")

        for task_info in project_plan:
            # ... (The rest of this logic is the same as the old execute_job method)
            guild = task_info["guild"]
            task_prompt = task_info["prompt"]

            for key, value in current_job.artifacts.items():
                placeholder = f"{{{key.upper()}}}"
                task_prompt = task_prompt.replace(placeholder, value)

            print(f"\nExecuting sub-task for {guild}'s Guild: '{task_prompt[:50]}...'")

            if guild == "Coder":
                result = self.execute_single_coder_task(task_prompt)
                # Save artifact with a generic name based on guild
                current_job.artifacts['code'] = result
            elif guild == "Writer":
                result = self.execute_single_writer_task(task_prompt)
                current_job.artifacts['report'] = result

            if not result:
                # ... (error handling) ...
                return None, current_job.history

            current_job.add_history("Monarch", f"Completed {guild} sub-task", result)

        current_job.status = "COMPLETED"
        return current_job.artifacts, current_job.history

    def execute_single_coder_task(self, prompt):
        """Gets the best coder and performs a single task."""
        # For simplicity, we get a C-rank engineer for any coding task now
        agent = self.get_agent("Software Engineer", "C")
        result = agent.perform_task(prompt)
        if result: agent.gain_xp(20)
        return result

    def execute_single_writer_task(self, prompt):
        """Gets the best writer and performs a single task."""
        # We'll use a C-rank writer for any writing task
        agent = self.get_agent("Writer", "C")
        result = agent.perform_task(prompt)
        if result: agent.gain_xp(20)
        return result



        # --- NEW ORCHESTRATION METHOD ---

    # def execute_writer_job(self, current_job):
    #     """Manages a multi-step job using a hierarchy of agents."""
    #     try:
    #         # Step 1: Outlining by a Researcher (Rank F+)
    #         outliner = self.get_agent("Researcher", "F")
    #         outline_prompt = f"Create a concise, bulleted outline for a report on the following topic: {current_job.user_request}"
    #         outline = outliner.perform_task(outline_prompt)
    #         if not outline: raise Exception("Outlining failed.")
    #         current_job.artifacts['outline'] = outline
    #         current_job.add_history(outliner.agent_id, "Generated Outline", outline)
    #         outliner.gain_xp(10)
    #
    #         # Step 2: Drafting by a Writer (Rank C+)
    #         writer = self.get_agent("Writer", "C")
    #         draft_prompt = f"Using the following outline, write a detailed draft of the report. \n\nOUTLINE:\n{outline}"
    #         draft = writer.perform_task(draft_prompt)
    #         if not draft: raise Exception("Drafting failed.")
    #         current_job.artifacts['draft'] = draft
    #         current_job.add_history(writer.agent_id, "Wrote Draft", draft)
    #         writer.gain_xp(25)  # More complex tasks grant more XP
    #
    #         # Step 3: Editing by an Editor (Rank A+)
    #         editor = self.get_agent("Editor", "A")
    #         edit_prompt = f"Review the following draft for clarity, accuracy, and style. Polish it into a final report. \n\nDRAFT:\n{draft}"
    #         final_report = editor.perform_task(edit_prompt)
    #         if not final_report: raise Exception("Editing failed.")
    #         current_job.artifacts['final_report'] = final_report
    #         current_job.add_history(editor.agent_id, "Finalized Report", final_report)
    #         editor.gain_xp(50)
    #
    #         current_job.status = "COMPLETED"
    #         print(f"\nJob {current_job.id} completed successfully!")
    #         return final_report, current_job.history
    #
    #     except Exception as e:
    #         current_job.status = "FAILED"
    #         print(f"Job {current_job.id} failed. Error: {e}")
    #         return None, current_job.history
    #
    # def execute_coder_job(self, current_job):
    #     """Handles the multi-step process for the Coder's Guild."""
    #     try:
    #         # Step 1: Planning by a Junior Dev (Rank F+)
    #         planner = self.get_agent("Junior Dev", "F")
    #         plan_prompt = f"Create a simple, step-by-step plan in plain English to create a Python script for the following request. Do not write any code. Request: {current_job.user_request}"
    #         plan = planner.perform_task(plan_prompt)
    #         if not plan: raise Exception("Planning failed.")
    #         current_job.artifacts['plan'] = plan
    #         current_job.add_history(planner.agent_id, "Created Plan", plan)
    #         planner.gain_xp(10)
    #
    #         # Step 2: Implementation by a Software Engineer (Rank C+)
    #         coder = self.get_agent("Software Engineer", "C")
    #         code_prompt = f"Based on the following plan, write the complete Python code. Only write the code, nothing else. \n\nPLAN:\n{plan}"
    #         code = coder.perform_task(code_prompt)
    #         if not code: raise Exception("Implementation failed.")
    #         current_job.artifacts['code'] = code
    #         current_job.add_history(coder.agent_id, "Wrote Code", code)
    #         coder.gain_xp(25)
    #
    #         # Step 3: Testing by a System Architect (Rank A+)
    #         tester = self.get_agent("System Architect", "A")
    #         test_prompt = f"Review the following Python code. First, explain any potential bugs or improvements. Second, write a simple test case to verify its functionality. \n\nCODE:\n{code}"
    #         review = tester.perform_task(test_prompt)
    #         if not review: raise Exception("Testing failed.")
    #         current_job.artifacts['review'] = review
    #         current_job.add_history(tester.agent_id, "Reviewed and Tested Code", review)
    #         tester.gain_xp(50)
    #
    #         current_job.status = "COMPLETED"
    #         final_product = f"--- PLAN ---\n{plan}\n\n--- CODE ---\n{code}\n\n--- REVIEW & TESTS ---\n{review}"
    #         print(f"\nCoder Guild Job {current_job.id} completed successfully!")
    #         return final_product, current_job.history
    #
    #     except Exception as e:
    #         current_job.status = "FAILED"
    #         print(f"Coder Guild Job {current_job.id} failed. Error: {e}")
    #         return None, current_job.history