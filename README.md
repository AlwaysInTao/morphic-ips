# Morphic-IPS: Active Network Defense & Detection Engine

Morphic-IPS is a proactive, low-overhead Intrusion Detection and Prevention System (IDS/IPS) built to dynamically isolate and manipulate adversarial traffic in real-time. Unlike traditional passive detection engines, this tool introduces active defense hooks that structurally decouple and alter host infrastructure when an exploit signature or scanning behavior is identified.

## 🛠️ System Architecture

The application is split into decoupled layers providing independent network tracking, live telemetry, policy orchestrations, and an administrative control panel:

*   **Active Defense Core (`engine.py`):** The primary pipeline executing traffic inspection loops, iptables management, policy state transitions, and asynchronous trigger monitoring.
*   **Morphic Control Center Dashboard (`gui_dashboard.py` / `dashboard.py`):** A custom local UI engine providing console status updates, system clock syncing, target rule status, and an interactive telemetry stream viewer.
*   **Web Portal Admin Console (`processor.php` / `index.html`):** A secure, session-tracked browser portal serving as the administrative head for system metrics monitoring and configuration adjustments.
*   **State Purge Control (`flush.sh`):** A low-level shell script engineered to safely tear down active iptables rule chains, restore baseline routing configurations, and flush session caches.

## ⚡ Active Defense Mitigation Policies

The platform currently implements three selectable defensive postures to handle incoming scanning profiles or unauthorized telemetry access:

*   **Active Spoofing:** Dynamic data-layer payload injection designed to feed anomalous, corrupted, or decoy telemetry blocks back to an active threat agent to disrupt scanning tools.
*   **Passive Tracking (Ignore):** Standby observation mode that tracks, logs, and indexes source IP telemetry, hardware fingerprints, and timing data without altering routing paths.
*   **Port Shifting:** A structural defensive mechanism that hooks loopback and edge traffic arriving on vulnerable listening slots (e.g., port `8080`), automatically redirecting threat loops to high-port traps (e.g., port `9999`) while completely dropping connection vectors from unauthorized hosts.

## 🚀 Installation & Baseline Deployment

### Prerequisites
*   Linux OS environment (tested on Ubuntu/Debian variations)
*   Python 3.x core interpreter
*   `iptables` firewall utilities with `sudo` execution privileges
*   PHP runtime (for web-facing portal processing blocks)

### Initialization Sequence
1. Clone the project locally and jump into the engine tree:
   ```bash
   cd ~/mini_ids
   ```
2. Initialize the background active scanning engine:
   ```bash
   sudo python3 engine.py
   ```
3. Launch the live Morphic Control Center tracking console:
   ```bash
   python3 gui_dashboard.py
   ```

---
*Maintained under local developer profile tracking. Future updates will introduce automated honeypot integration pools and polymorphic rule generation arrays.*
