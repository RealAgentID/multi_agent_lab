import os
import json
import time
import redis

# Connect to Redis
redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Load RealAgentID config
config_path = os.getenv("REALAGENTID_CONFIG", "/opt/realagentid/agents.json")
with open(config_path, "r") as f:
    REALAGENTID = json.load(f)

REGISTER_CHANNEL = "agent_register"
TASK_CHANNEL = "task_queue"

print("Orchestrator started. Waiting for agents...")

def verify_agent(agent_id):
    """Check if the agent exists in RealAgentID config."""
    return agent_id in REALAGENTID

def verify_permission(agent_id, action):
    """Check if the agent is allowed to perform the action."""
    agent = REALAGENTID.get(agent_id, {})
    allowed = agent.get("permissions", [])
    denied = agent.get("denied", [])

    if action in denied:
        return False

    return action in allowed

def main():
    pubsub = r.pubsub()
    pubsub.subscribe(REGISTER_CHANNEL, TASK_CHANNEL)

    registered_agents = {}

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        channel = message["channel"]
        data = message["data"]

        # Agent registration
        if channel == REGISTER_CHANNEL:
            agent_info = json.loads(data)
            agent_id = agent_info.get("agent_id")

            if verify_agent(agent_id):
                registered_agents[agent_id] = agent_info
                print(f"[REGISTERED] {agent_id}")
            else:
                print(f"[REJECTED] Unknown agent attempted to register: {agent_id}")

        # Task routing
        elif channel == TASK_CHANNEL:
            task = json.loads(data)
            target_agent = task.get("target_agent")
            action = task.get("action")

            if not verify_agent(target_agent):
                print(f"[BLOCKED] Task sent to unknown agent: {target_agent}")
                continue

            if not verify_permission(target_agent, action):
                print(f"[DENIED] {target_agent} attempted forbidden action: {action}")
                continue

            # Forward task to the agent's queue
            agent_queue = f"queue:{target_agent}"
            r.lpush(agent_queue, json.dumps(task))
            print(f"[TASK] Routed to {target_agent}: {action}")

if __name__ == "__main__":
    main()
