#!/usr/bin/env python3
import json
import os
import subprocess
import time
import random

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
TRIGGER_PATH = os.path.join(WORKSPACE_DIR, 'ids_trigger.json')
HISTORY_LOG = '/var/log/mini_ids/history.json'
CONFIG_PATH = '/etc/mini_ids/config.json'

print(f"[*] Mini-IDS Active Engine Online. Monitoring path: {TRIGGER_PATH}")

try:
    while True:
        if os.path.exists(TRIGGER_PATH):
            time.sleep(0.2)
            try:
                with open(TRIGGER_PATH, 'r') as f:
                    alert = json.load(f)
                
                ip = alert['attacker_ip']
                hw_hash = alert['hardware_fingerprint']
                
                if os.path.exists(CONFIG_PATH):
                    with open(CONFIG_PATH, 'r') as f:
                        defense_mode = json.load(f).get("defense_mode", "ACTIVE SPOOFING")
                else:
                    defense_mode = "ACTIVE SPOOFING"
                
                print(f"[!] Processing alert for IP: {ip} | Mode: {defense_mode}")
                
                if defense_mode == "ACTIVE SPOOFING":
                    # 1. Define a pool of realistic, varying OS TTL fingerprints
                    # 64 = Standard Linux/Android, 128 = Windows, 255 = Cisco/Solaris Router
                    spoof_profiles = [64, 128, 255, 45, 98] 
                    selected_ttl = random.choice(spoof_profiles)
                    
                    print(f"[*] Polymorphic Action: Shuffling TCP signature to TTL {selected_ttl} for target {ip}")
                    
                    # 2. Clear old spoofing rules for this IP to prevent stack pollution
                    subprocess.run(f"sudo iptables -t mangle -D POSTROUTING -d {ip} -p tcp -j TTL --ttl-set 64 2>/dev/null", shell=True)
                    subprocess.run(f"sudo iptables -t mangle -D POSTROUTING -d {ip} -p tcp -j TTL --ttl-set 128 2>/dev/null", shell=True)
                    subprocess.run(f"sudo iptables -t mangle -D POSTROUTING -d {ip} -p tcp -j TTL --ttl-set 255 2>/dev/null", shell=True)
                    
                    # 3. Inject the newly chosen random fingerprint
                    subprocess.run(f"sudo iptables -t mangle -A POSTROUTING -d {ip} -p tcp -j TTL --ttl-set {selected_ttl}", shell=True)
                    
                    # 4. Throw a sleek, non-intrusive Zenity Info Toast notification on screen
                    zenity_toast = f'DISPLAY=:0 zenity --info --title="IDS Spoof Active" --text="Polymorphic Shift deployed for IP {ip}\nIdentity masked to TTL: {selected_ttl}" --timeout=3'
                    subprocess.run(zenity_toast, shell=True)

                elif defense_mode == "PORT SHIFTING":
                    subprocess.run(f"sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 8080 -j REDIRECT --to-ports 9999", shell=True)
                    subprocess.run(f"sudo ip6tables -t nat -A OUTPUT -o lo -p tcp --dport 8080 -j REDIRECT --to-ports 9999", shell=True)
                    print("[+] Port Shifting mitigations deployed.")
                    
                    zenity_text = f"🚨 SECURITY INTRUSION TRAPPED! 🚨\n\nSource IP Address: {ip}\nHardware Signature: {hw_hash}\n\nThe Port Shifting firewall block has been actively engaged."
                    zenity_cmd = f'DISPLAY=:0 zenity --question --title="Mini-IDS Intrusion Alert" --text="{zenity_text}" --ok-label="Open Workspace Terminal" --cancel-label="Dismiss Alert"'
                    response = subprocess.run(zenity_cmd, shell=True)
                    if response.returncode == 0:
                        subprocess.run('gnome-terminal -- bash -c "echo \\"=== INTRUSION ANALYSIS TOOLBOX ===\\"; echo \\"\\"; echo \\"Active Loopback iptables Redirect Rules:\\"; sudo iptables -t nat -L OUTPUT -v -n; echo \\"\\"; echo \\"To flush this rule block when done, run: ./flush.sh\\"; exec bash"', shell=True)

                with open(HISTORY_LOG, 'a') as f:
                    f.write(json.dumps(alert) + '\n')
                    
                if os.path.exists(TRIGGER_PATH):
                    os.remove(TRIGGER_PATH)
                
            except Exception as e:
                print(f"[-] Parse Error: {e}")
                if os.path.exists(TRIGGER_PATH):
                    os.remove(TRIGGER_PATH)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n[*] Engine shutting down.")
