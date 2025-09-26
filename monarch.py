# monarch.py
import json
from agent import ShadowAgent, RANKS
from Job import Job


class Monarch:
    def __init__(self, army_file="army.json", guild_config_file="guilds.json"):
        self.army = {}
        self.army_file = army_file
        self.specialty_counter={}
        self._load_guild_configs(guild_config_file)
        self._load_army()
        print(f"Monarch System Initialized. Managing {len(self.army)} agents across {len(self.guilds)} guilds.")

    def _load_guild_configs(self, guild_config_file):
        """Loads the guild definitions from the config file."""
        with open(guild_config_file, 'r') as f:
            self.guilds = json.load(f)

    def _determine_guild(self, user_request):
        """Dynamically determines the guild by checking keywords from the config."""
        prompt = user_request.lower()
        for guild_name, config in self.guilds.items():
            if any(keyword in prompt for keyword in config["keywords"]):
                return guild_name, config
        return "Writer", self.guilds["Writer"]  # Default to Writer

    def get_agent(self, specialty, guild_config, min_rank="F"):
        """Finds an existing qualified agent or creates a NEW F-Rank beginner."""
        # Find the best available agent that meets the minimum rank
        best_agent = None
        for agent in self.army.values():
            if agent.specialty == specialty and RANKS.index(agent.rank) >= RANKS.index(min_rank):
                if best_agent is None or RANKS.index(agent.rank) > RANKS.index(best_agent.rank):
                    best_agent = agent

        if best_agent:
            print(f"Monarch: Found available agent {best_agent.agent_id} for the job.")
            return best_agent

        # --- NEW LOGIC: Only create agents at the starting role ---
        start_role = guild_config.get("start_role")
        if specialty == start_role:
            print(f"Monarch: No available '{specialty}'. Recruiting a new F-Rank agent.")
            # Logic to create a new agent (always at F-Rank)
            current_count = self.specialty_counter.get(specialty, 0) + 1
            self.specialty_counter[specialty] = current_count
            agent_id = f"{specialty[0]}-{current_count:03d}"
            new_agent = ShadowAgent(agent_id, "F", specialty, guild_config)
            self.army[agent_id] = new_agent
            return new_agent
        else:
            # If a high-level specialist is needed but doesn't exist, we cannot create one.
            return None

        # In monarch.py, inside the Monarch class

    def execute_job(self, user_request):
        """
        Handles a user request with a flexible approach. Tries the full workflow first,
        then falls back to the best available agent if needed.
        """
        guild_name, guild_config = self._determine_guild(user_request)
        current_job = Job(user_request)
        print(f"Monarch: Task assigned to the {guild_name}'s Guild.")

        # --- Try the full, complex workflow first ---
        workflow = guild_config["workflow"]
        can_execute_full_workflow = True
        for step in workflow:
            agent = self.get_agent(step["role"], guild_config, step["min_rank"])
            if not agent:
                can_execute_full_workflow = False
                break

        if can_execute_full_workflow:
            print("Monarch: Qualified agents found for all steps. Executing full workflow.")
            for step in workflow:
                # ... (This is the same workflow logic as before)
                role = step["role"]
                min_rank = step["min_rank"]
                task_prompt = step["task"]
                artifact_name = step["artifact_name"]
                for key, value in current_job.artifacts.items():
                    task_prompt = task_prompt.replace(f"{{{key}}}", value)
                task_prompt = task_prompt.replace("{request}", user_request)
                agent = self.get_agent(role, guild_config, min_rank)
                result = agent.perform_task(task_prompt) if guild_name != "Artist" else agent.create_image(
                        task_prompt)
                if not result:
                    current_job.status = "FAILED"
                    return None, current_job.history
                current_job.artifacts[artifact_name] = result
                current_job.add_history(agent.agent_id, f"Completed step: {role}", result)
                agent.gain_xp(20)

            final_artifact_name = workflow[-1]["artifact_name"]
            return current_job.artifacts.get(final_artifact_name), current_job.history

        else:
            # --- FALLBACK: "Best Effort" Mode ---
            print(
                "Monarch: High-rank specialists not available. Assigning to best available agent for a single-step completion.")
            start_role = guild_config["start_role"]
            agent = self.get_agent(start_role, guild_config)  # Get the best available beginner

            result = agent.perform_task(user_request) if guild_name != "Artist" else agent.create_image(
                user_request)

            if result:
                agent.gain_xp(25)  # Give a larger XP boost for handling a complex task alone
                return result, [f"Completed by best-effort agent {agent.agent_id}"]
            else:
                return None, [f"Best-effort attempt by {agent.agent_id} failed."]

    def _load_army(self):
        """Loads the army state, handling missing or empty files."""
        try:
            with open(self.army_file, 'r') as f:
                content = f.read()
                if not content:  # Check if the file is empty
                    print("Army file is empty. Starting with a new army.")
                    return  # Exit the method

                army_data = json.loads(content)
                for agent_id, data in army_data.items():
                    specialty = data['specialty']
                    guild_config = None
                    for config in self.guilds.values():
                        if specialty in config['prompts']:
                            guild_config = config
                            break

                    if guild_config:
                        agent = ShadowAgent(data['agent_id'], data['rank'], specialty, guild_config)
                        agent.xp = data['xp']
                        self.army[agent_id] = agent
        except FileNotFoundError:
            print("No existing army file found. Starting with a new army.")
        except Exception as e:
            print(f"Could not load army file. Starting fresh. Error: {e}")

    def save_army(self):
        with open(self.army_file, 'w') as f:
            army_data = {id: agent.to_dict() for id, agent in self.army.items()}
            json.dump(army_data, f, indent=4)
        print("Army state saved.")