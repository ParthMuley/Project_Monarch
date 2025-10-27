# monarch.py
import json
from agent import ShadowAgent, RANKS, RANK_XP_THRESHOLDS
from job import Job
from memory import memorize


class Monarch:
    def __init__(self, army_file="army.json", guild_config_file="guilds.json", main_config_file="config.json"):
        self.army = {}
        self.army_file = army_file
        self.guild_config_file = guild_config_file
        self.main_config_file = main_config_file
        self.specialty_counters = {}

        # Load main config first
        with open(main_config_file, 'r') as f:
            self.config = json.load(f)
        self.treasury = self.config.get("treasury", 500)

        self._load_guild_configs(guild_config_file)
        self._load_army()

        print(
            f"Monarch System Initialized. Treasury: ${self.treasury}. Managing {len(self.army)} agents across {len(self.guilds)} guilds.")

    def _load_guild_configs(self, guild_config_file):
        """Loads the guild definitions from the config file."""
        with open(guild_config_file, 'r') as f:
            self.guilds = json.load(f)

    def _determine_guild(self, user_request):
        """Dynamically determines the guild by checking for specific keywords first."""
        prompt = user_request.lower()

        # Prioritize Coder and Artist guilds as their keywords are more specific.
        if any(keyword in prompt for keyword in self.guilds["Coder"]["keywords"]):
            return "Coder", self.guilds["Coder"]
        if any(keyword in prompt for keyword in self.guilds["Artist"]["keywords"]):
            return "Artist", self.guilds["Artist"]
        # Default to Writer if no other specific keywords are found.
        return "Writer", self.guilds["Writer"]

    def _get_agent(self, specialty, guild_config, min_rank="F"):
        """Finds the most cost-effective agent that meets the minimum rank."""

        qualified_agents = []
        for agent in self.army.values():
            if agent.specialty == specialty and RANKS.index(agent.rank) >= RANKS.index(min_rank):
                qualified_agents.append(agent)

        if qualified_agents:
            # Sort agents by rank (cheapest first) and pick the first one
            qualified_agents.sort(key=lambda x: RANKS.index(x.rank))
            cheapest_agent = qualified_agents[0]
            print(
                f"Monarch: Found {len(qualified_agents)} qualified agents. Choosing the most cost-effective: {cheapest_agent.agent_id} ({cheapest_agent.rank} Rank).")
            return cheapest_agent

        # --- Creation logic remains the same ---
        start_role = guild_config.get("start_role")
        if specialty == start_role:
            print(f"Monarch: No available '{specialty}'. Recruiting a new F-Rank agent.")
            current_count = self.specialty_counters.get(specialty, 0) + 1
            self.specialty_counters[specialty] = current_count
            agent_id = f"{specialty[0]}-{current_count:03d}"
            new_agent = ShadowAgent(agent_id, "F", specialty, guild_config)
            self.army[agent_id] = new_agent
            return new_agent
        else:
            return None


    def _is_agent_available(self, specialty, min_rank):
        """Checks if a qualified agent exists without creating one."""
        for agent in self.army.values():
            if agent.specialty == specialty and RANKS.index(agent.rank) >= RANKS.index(min_rank):
                return True
        return False

        # In monarch.py, this is the complete, final version of the execute_job method

    def _estimate_difficulty(self, user_request):
        """A simple keyword-based difficulty estimator."""
        prompt = user_request.lower()
        if any(kw in prompt for kw in ["complex", "application", "game", "report"]):
            return "Hard"
        if any(kw in prompt for kw in ["summary", "function", "logo"]):
            return "Medium"
        return "Easy"

    def execute_job(self, user_request):
        """
        Intelligently handles a request, including dynamic difficulty, rewards,
        penalties, and a full economic model.
        """
        guild_name, guild_config = self._determine_guild(user_request)
        current_job = Job(user_request)
        job_cost = 0

        difficulty = self._estimate_difficulty(user_request)
        job_tier_info = self.config["job_tiers"][difficulty] # Reads from config.json now
        job_reward = job_tier_info["reward"]
        job_penalty = job_tier_info["penalty"]

        print(f"Monarch: Job estimated as '{difficulty}' difficulty. Reward: ${job_reward}, Penalty: ${job_penalty}")

        # --- CAPABILITY ASSESSMENT ---
        workflow = guild_config["workflow"]
        can_execute_full_workflow = True
        for step in workflow:
            if not self._is_agent_available(step["role"], step["min_rank"]):
                can_execute_full_workflow = False
                break

        # --- EXECUTION BASED ON ASSESSMENT ---
        if can_execute_full_workflow:
            print("Monarch: Qualified specialists found. Executing full multi-step workflow.")
            final_product = None
            for step in workflow:
                role, min_rank, task_prompt, artifact_name = step["role"], step["min_rank"], step["task"], step["artifact_name"]
                for key, value in current_job.artifacts.items():
                    task_prompt = task_prompt.replace(f"{{{key}}}", value)
                task_prompt = task_prompt.replace("{request}", user_request)
                agent = self._get_agent(role, guild_config, min_rank)
                if not agent:
                    current_job.status = "FAILED"; break

                agent_cost = self.config["rank_costs"].get(agent.rank, 20)
                if self.treasury < agent_cost:
                    print(f"Job failed: Not enough funds for agent. Cost: ${agent_cost}, Treasury: ${self.treasury}.")
                    current_job.status = "FAILED"; break
                self.treasury -= agent_cost
                job_cost += agent_cost
                print(f"Monarch: Assigning agent {agent.agent_id}. Cost: ${agent_cost}. Treasury Left: ${self.treasury}")

                result_data = agent.perform_task(task_prompt) if guild_name != "Artist" else {"response": agent.create_image(task_prompt), "tool_used": None}
                result = result_data["response"]
                tool_used = result_data["tool_used"]

                if tool_used:
                    tool_cost = self.config["tool_costs"].get(tool_used, 0)
                    if self.treasury < tool_cost:
                        print(f"Job failed: Not enough funds for tool. Cost: ${tool_cost}, Treasury: ${self.treasury}.")
                        current_job.status = "FAILED"; break
                    self.treasury -= tool_cost
                    job_cost += tool_cost
                    print(f"Monarch: Deducted ${tool_cost} for tool '{tool_used}'. Treasury Left: ${self.treasury}")

                if not result:
                    current_job.status = "FAILED"; break

                current_job.artifacts[artifact_name] = result
                # --- RE-ADD THESE LINES ---
                current_job.add_history(agent.agent_id, f"Completed step: {role}", result)
                agent.gain_xp(20)
                # -------------------------

            final_artifact_name = workflow[-1]["artifact_name"]
            final_product = current_job.artifacts.get(final_artifact_name)

            if current_job.status == "FAILED" or not final_product:
                self.treasury -= job_penalty
                print(f"Job failed. Penalty of ${job_penalty} deducted. New Treasury Balance: ${self.treasury}")
                return None, current_job.history
            else:
                self.treasury += job_reward
                print(f"Job successful. Reward of ${job_reward} earned. New Treasury Balance: ${self.treasury}")
                memorize(job_id=current_job.id, content=final_product)
                return final_product, current_job.history
        else:
            # --- FALLBACK: "Best Effort" Mode ---
            print("Monarch: High-rank specialists not available. Falling back to 'Best Effort' mode.")
            start_role = guild_config["start_role"]
            agent = self._get_agent(start_role, guild_config, "F")

            agent_cost = self.config["rank_costs"].get(agent.rank, 20)
            if self.treasury < agent_cost:
                print(f"Job failed on Best Effort: Not enough funds.")
                return None, ["Best-effort attempt failed due to budget."]
            self.treasury -= agent_cost
            job_cost += agent_cost # Use job_cost here
            print(f"Monarch: Assigning agent {agent.agent_id}. Cost: ${agent_cost}. Treasury Left: ${self.treasury}")

            result_data = agent.perform_task(user_request) if guild_name != "Artist" else {"response": agent.create_image(user_request), "tool_used": None}
            result = result_data["response"]
            tool_used = result_data["tool_used"]

            if tool_used:
                tool_cost = self.config["tool_costs"].get(tool_used, 0)
                if self.treasury < tool_cost:
                    print(f"Job failed: Not enough funds for tool '{tool_used}'.")
                    return None, current_job.history
                self.treasury -= tool_cost
                job_cost += tool_cost
                print(f"Monarch: Deducted ${tool_cost} for tool '{tool_used}'. Treasury Left: ${self.treasury}")

            if not result:
                self.treasury -= job_penalty
                print(f"Job failed (Best Effort). Penalty of ${job_penalty} deducted. New Treasury Balance: ${self.treasury}")
                return None, [f"Best-effort attempt by {agent.agent_id} failed."]
            else:
                self.treasury += job_reward
                print(f"Job successful (Best Effort). Reward of ${job_reward} earned. New Treasury Balance: ${self.treasury}")
                # --- RE-ADD THESE LINES ---
                agent.gain_xp(25)
                current_job.add_history(agent.agent_id, "Completed job via Best Effort", result)
                # -------------------------
                memorize(job_id=current_job.id, content=result)
                return result, current_job.history

    def _load_army(self):
        """Loads the army state and correctly recalculates rank from XP."""
        try:
            with open(self.army_file, 'r') as f:
                content = f.read()
                if not content: return

                army_data = json.loads(content)
                for agent_id, data in army_data.items():
                    specialty = data['specialty']
                    agent_guild_config = None

                    # --- CORRECTED LOGIC ---
                    # Find which guild this agent belongs to by checking the specialty
                    for guild_name, config in self.guilds.items():
                        # Add a check to ensure the config is a dictionary (a guild)
                        if isinstance(config, dict) and specialty in config.get('prompts', {}):
                            agent_guild_config = config
                            break
                    # --- END OF CORRECTION ---

                    if agent_guild_config:
                        agent = ShadowAgent(data['agent_id'], "F", specialty, agent_guild_config)
                        agent.xp = data['xp']
                        # Recalculate true rank
                        for rank in RANKS:
                            if agent.xp >= RANK_XP_THRESHOLDS.get(rank, float('inf')):
                                agent.rank = rank
                            else:
                                break
                        agent.update_config()
                        self.army[agent_id] = agent
                        print(f"-> Loaded veteran agent: {agent.agent_id} ({agent.rank} Rank, {agent.xp} XP)")

        except FileNotFoundError:
            print("No existing army file found. Starting with a new army.")

    def save_army(self):
        with open(self.army_file, 'w') as f:
            army_data = {id: agent.to_dict() for id, agent in self.army.items()}
            json.dump(army_data, f, indent=4)
        print("Army state saved.")

    def save_configs(self):
        """Saves the updated treasury back to the correct config.json file."""
        self.config["treasury"] = self.treasury
        with open(self.main_config_file, 'w') as f: # <-- USE THE CORRECT FILENAME
            json.dump(self.config, f, indent=2)
        print(f"Configs saved. New treasury balance: ${self.treasury}")