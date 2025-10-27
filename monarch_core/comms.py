# monarch_core/comms.py
from collections import defaultdict

# A simple in-memory message queue.
# defaultdict(list) creates a dictionary where each value is automatically a list.
_message_queue = defaultdict(list)

def send_message(recipient_id: str, sender_id: str, message_content: str):
    """Adds a message to the recipient's queue."""
    _message_queue[recipient_id].append({
        "sender": sender_id,
        "content": message_content
    })
    print(f"--- Comms: Message sent from {sender_id} to {recipient_id} ---")

def check_messages(agent_id: str) -> list:
    """Retrieves and clears all messages for a specific agent."""
    messages = _message_queue.pop(agent_id, []) # Get messages and remove them
    if messages:
        print(f"--- Comms: Agent {agent_id} received {len(messages)} message(s) ---")
    return messages