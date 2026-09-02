#!/bin/bash
# Sub-Interface Hopping Protocol

INTERFACE="lo" # Loopback or your local Ethernet adapter
SUBNET="127.0"
CURRENT_IP="1"

while true; do
    # Generate a random host identifier between 100 and 200
    NEW_IP=$((100 + RANDOM % 101))
    
    # Tear down old virtual sub-interface safely
    sudo ip addr del ${SUBNET}.0.${CURRENT_IP}/8 dev ${INTERFACE} 2>/dev/null
    
    # Bring up the new dynamic hop interface
    CURRENT_IP=${NEW_IP}
    TARGET_IP="${SUBNET}.0.${CURRENT_IP}"
    sudo ip addr add ${TARGET_IP}/8 dev ${INTERFACE}
    
    echo "[*] Morphic Layer Shifted: Admin Dashboard now running on ${TARGET_IP}"
    
    # Keep the interface stable for 60 seconds before shifting again
    sleep 60
done
