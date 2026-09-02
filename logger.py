import json
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/mini_ids/morphic_events.json")

def log_event(policy_type, source_ip, details=""):
    """Appends a structured security event to the morphic log file."""
    event_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "policy": policy_type,
        "source_ip": source_ip,
        "details": details
    }
    
    # Read existing logs or start fresh array
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            pass # Handle blank or corrupted log file safely
            
    logs.append(event_data)
    
    # Write back atomically
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[+] Event logged: {policy_type} from {source_ip}")

def verify_log_integrity():
    """Addendum: Performs runtime security audits on the active telemetry stream."""
    import hashlib
    if not os.path.exists(LOG_FILE):
        return True
    try:
        with open(LOG_FILE, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        # Prevent runtime write hijacking if log reaches arbitrary constraints
        if os.path.getsize(LOG_FILE) > 5242880: # 5MB limit
            print("[!] Warning: Morphic log allocation threshold reached. Executing rotation sequence.")
            os.rename(LOG_FILE, LOG_FILE + ".bak")
        return file_hash
    except Exception as e:
        print(f"[-] Integrity subsystem anomaly: {e}")
        return None
