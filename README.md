# 🛡️ Mini-IDS/IPS Engine: Multi-User Network Security Suite

Welcome to the **Mini-IDS/IPS Engine** repository! This open-source network security engine captures raw incoming network data, extracts TCP/IP socket structures, and flags malicious payloads against custom pattern signatures. 

The architecture has been recently refactored to support a fully decentralized, **multi-user deployment framework** capable of ingesting industry-standard rulesets while guarding system stability with real-time hardware safety switches.

---

## 🚀 Core Security Features

* **Raw Socket Sniffing:** Hooks directly into the system network interface loop to inspect lower-level IP structures natively.
* **Suricata Engine & Ingestion Pipeline:** Ingests standard flat-text Suricata rule signatures in bulk, normalizes them, and syncs them to a shared rules manifest database.
* **Decentralized Multi-User Tracking:** Tracks rule deployment states natively. When a team member globally applies or decommissions a rule, it signs the action with their username and a timestamp so other users see changes in real time.
* **Defensive Safety Throttling:** Includes a hardware-protection throttle. If a loopback packet broadcast flood occurs, the engine self-governs its loop cycle speed to protect your CPU and memory from locking up.
* **Zero Dependencies:** Engineered completely via native Python libraries (`socket`, `struct`, and `argparse`) for absolute portability.

---

## ⚙️ Command-Line Utilities

The engine includes integrated terminal utilities to manage the multi-user manifest data structure without opening file editors.

### 1. View Global Rules Layout
Queries the shared database to display active rules, ports, and deployment owners:
```bash
python3 engine.py --list-rules
```

### 2. Ingest Signatures in Bulk
Reads standard text rule definitions from an external file and compiles them cleanly into the rules environment:
```bash
python3 engine.py --sync /path/to/signatures.rules
```

### 3. Toggle Rule Deployments
Enforces or removes a rule state globally. The action is signed instantly across all multi-user endpoints:
```bash
python3 engine.py --toggle <signature_id> <username> <apply|remove>
```

### 4. Run the Network Engine
Fires up live raw packet extraction on the loopback or target interface:
```bash
sudo python3 engine.py --run
```
*(Note: Because raw network interface capture requires kernel administration hook-access, running the sniffing engine requires `sudo`).*

---

## ⚙️ Persistent Deployment (Run Automatically at Boot)

To run the Mini-IDS/IPS Engine automatically as a background security service on Linux, configure a native `systemd` service:

1. Create a service configuration file:
```bash
sudo nano /etc/systemd/system/mini-ids.service
```

2. Paste the following configuration into the file (make sure to replace `/home/brian/mini_ids/` with the actual path to your repository):
```ini
[Unit] Description=Mini IDS/IPS Reactive Moving Target Defense Daemon After=network.target [Service] Type=simple WorkingDirectory=/home/brian/mini_ids User=root ExecStartPre=-/usr/bin/killall python3 ExecStart=/usr/bin/python3 /home/brian/mini_ids/engine.py --run Restart=on-failure [Install] WantedBy=multi-user.target
```

3. Reload the system controller daemon, enable the service to start at boot, and fire it up immediately:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mini-ids.service
sudo systemctl start mini-ids.service
```

4. To monitor live security alerts or debug the engine running in the background, read the system journals:
```bash
sudo journalctl -u mini-ids.service -f
```

---

## 🧠 Acknowledgments
* Co-designed and documented in partnership with Gemini AI.
