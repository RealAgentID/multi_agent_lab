import json
import time
from datetime import datetime

LOG_PATH = "/var/log/realagentid/agent-actions.log"

def log_action(agent_id, action, scope=None, status="success", details=None):
    """Write a structured RealAgentID audit log entry."""

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "action": action,
        "scope": scope or {},
        "result": {
            "status": status,
            "details": details
        }
    }

    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[LOGGER ERROR] {e}")
