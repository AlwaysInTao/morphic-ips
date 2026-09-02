#!/bin/bash
echo "[*] Initializing network firewall reset..."
# 1. Flush specific tables used by the Mini-IDS/IPS
iptables -t nat -F PREROUTING
iptables -t nat -F OUTPUT
iptables -t mangle -F POSTROUTING
# 2. Clear out any lingering scheduled cleanup background tasks
atrm $(atq | cut -f1) 2>/dev/null
echo "[+] Mini-IDS rules vaporized cleanly. Network baseline restored."
