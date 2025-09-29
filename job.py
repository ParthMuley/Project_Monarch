# job.py

class Job:
    def __init__(self, user_request, budget=200): # Give each job a default budget
        self.id = id(self)  # Unique ID for the job
        self.user_request = user_request
        self.status = "PENDING"
        self.history = []  # To log each step
        self.artifacts = {}  # To store outputs like 'outline', 'draft'
        print(f"New Job created (ID: {self.id}) for request: '{self.user_request}'")

    def add_history(self, agent_id, action, result):
        """Adds a record of an action taken by an agent."""
        step_summary = result[:100] + '...' if len(result) > 100 else result
        self.history.append(f"[{agent_id}]: {action} -> '{step_summary}'")
        print(f"Job {self.id} Log: Agent {agent_id} completed '{action}'.")