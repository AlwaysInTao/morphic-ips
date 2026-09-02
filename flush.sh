#!/bin/bash
# Morphic-IPS Master Core Teardown & Reset Routine

echo "[*] Initializing Morphic Infrastructure Flush Sequence..."

# 1. Reset Linux firewall rules and tables safely
echo "[*] Purging active iptables redirection chains..."
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X

# 2. Flush dynamic loopback alias network sub-interfaces
echo "[*] Tearing down lingering virtual sub-interfaces..."
for ip in $(seq 100 200); do
    sudo ip addr del 127.0.0.1${ip}/8 dev lo 2>/dev/null
done

# 3. Terminate background Python monitoring and tarpit loops
echo "[*] Cleansing active python listener background PIDs..."
sudo pkill -f tarpit.py 2>/dev/null
sudo pkill -f decoy.py 2>/dev/null
sudo pkill -f simulate_attack.py 2>/dev/null

echo "[+] System baseline configuration restored successfully."
