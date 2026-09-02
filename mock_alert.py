import json
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/mini_ids/morphic_events.json")

# Draft a fake critical exploit pattern
mock_payload = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "policy": "PORT SHIFTING / TARPIT",
    "source_ip": "192.168.1.42",
    "details": "Aggressive TCP port scanning detected. Session locked down into slow-feed tarpit socket."
}

# Read existing log or initialize fresh array
logs = []
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        pass

logs.append(mock_payload)

with open(LOG_FILE, "w") as f:
    json.dump(logs, f, indent=4)

print("[+] Mock threat payload successfully written into active tracking streams.")
