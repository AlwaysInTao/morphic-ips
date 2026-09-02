import json
import os
import time
import socket
import struct
import sys

RULES_DIR = "rules"
MANIFEST_PATH = os.path.join(RULES_DIR, "rules_manifest.json")

def parse_suricata_rule(rule_string):
    """Parses a standard flat-text Suricata rule string into a structured dictionary."""
    if not rule_string.startswith("alert"):
        return None
    try:
        header, options = rule_string.split('(', 1)
        header_parts = header.strip().split()
        
        msg = "Custom Network Alert"
        if 'msg:"' in options:
            msg = options.split('msg:"')[1].split('"')[0]
            
        sid = str(int(time.time() * 1000))
        if 'sid:' in options:
            sid = options.split('sid:')[1].split(';')[0].strip()

        rule_dict = {
            "sid": sid,
            "protocol": header_parts[1].lower(),
            "src_ip": header_parts[2],
            "src_port": header_parts[3],
            "direction": header_parts[4],
            "dst_ip": header_parts[5],
            "dst_port": header_parts[6],
            "msg": msg,
            "status": "inactive",
            "applied_by": None,
            "applied_at": None,
            "description": msg
        }
        return rule_dict
    except Exception:
        return None

def sync_bulk_rules_file(text_file_path, current_user="System"):
    """Ingests text rules in bulk and merges them into the shared manifest."""
    if not os.path.exists(text_file_path):
        print(f"[-] Error: Source rule file '{text_file_path}' not found.")
        return

    os.makedirs(RULES_DIR, exist_ok=True)
    manifest = {"rules": {}}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, 'r') as f:
                manifest = json.load(f)
                if "rules" not in manifest:
                    manifest = {"rules": {}}
        except Exception:
            pass

    new_count = 0
    with open(text_file_path, 'r') as f:
        for line in f:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
                
            parsed = parse_suricata_rule(clean_line)
            if parsed:
                sid = parsed["sid"]
                if sid not in manifest["rules"]:
                    manifest["rules"][sid] = parsed
                    new_count += 1

    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)
    print(f"[+] Multi-user Manifest Synced: Ingested {new_count} new rules. Total: {len(manifest['rules'])}")

def toggle_rule_deployment(sid, username, action="apply"):
    """Allows a user to apply or remove a rule globally."""
    if not os.path.exists(MANIFEST_PATH):
        print("[-] Error: No rule manifest initialized yet.")
        return False

    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    if sid in manifest["rules"]:
        rule = manifest["rules"][sid]
        if action == "apply":
            rule["status"] = "active"
            rule["applied_by"] = username
            rule["applied_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[+] Rule {sid} globally ENFORCED by user: {username}")
        else:
            rule["status"] = "inactive"
            rule["applied_by"] = None
            rule["applied_at"] = None
            print(f"[-] Rule {sid} deactivated by user: {username}")
            
        with open(MANIFEST_PATH, 'w') as f:
            json.dump(manifest, f, indent=4)
        return True
    
    print(f"[-] Error: Signature ID {sid} not found in global tracking manifest.")
    return False

def check_packet_against_active_rules(protocol, src_ip, dst_port):
    """Matches raw network packet structures against globally deployed multi-user rules."""
    if not os.path.exists(MANIFEST_PATH):
        return

    try:
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
    except Exception:
        return

    for sid, rule in manifest.get("rules", {}).items():
        if rule["status"] != "active":
            continue

        proto_match = (rule["protocol"] == "any" or rule["protocol"] == protocol.lower())
        port_match = (rule["dst_port"] == "any" or str(rule["dst_port"]) == str(dst_port))
        
        if proto_match and port_match:
            print(f"\n[🚨 IPS ALERT - SID {sid}] {rule['msg']}")
            print(f"    Traffic Match: {src_ip} -> port {dst_port} ({protocol})")
            print(f"    Rule Enforced By: {rule['applied_by']} on {rule['applied_at']}\n")

def list_tracked_rules():
    """Reads the shared manifest and prints a scannable deployment grid layout."""
    if not os.path.exists(MANIFEST_PATH):
        print("[-] Quick Lookup Error: Shared rule manifest does not exist yet.")
        print("    Run a bulk sync first to populate signature records.")
        return

    try:
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[-] Failed to read manifest data structure: {e}")
        return

    rules = manifest.get("rules", {})
    if not rules:
        print("[*] The global rule tracking manifest is currently empty.")
        return

    print("\n" + "="*95)
    print(f" {'SID':<14} | {'PROTOCOL':<8} | {'PORT':<6} | {'STATUS':<10} | {'DEPLOYED BY':<15} | {'DESCRIPTION'}")
    print("="*95)

    for sid, rule in rules.items():
        status = rule.get("status", "inactive").upper()
        proto = rule.get("protocol", "any").upper()
        port = str(rule.get("dst_port", "any"))
        user = rule.get("applied_by") if rule.get("applied_by") else "Unassigned"
        desc = rule.get("description", rule.get("msg", ""))
        
        if len(desc) > 30:
            desc = desc[:27] + "..."

        print(f" {sid:<14} | {proto:<8} | {port:<6} | {status:<10} | {user:<15} | {desc}")
    print("="*95 + "\n")

def start_sniffer_engine(interface="lo", dry_run=True):
    """Main execution loop for capturing packets and passing them to rule checks."""
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sniffer.bind((interface, 0))
        sniffer.settimeout(1.0)
    except PermissionError:
        print("[-] Error: Administrative / Root privileges (sudo) required to capture packets.")
        return
    except Exception as e:
        print(f"[-] Failed to bind interface {interface}: {e}")
        return

    print(f"[*] Core IPS Engine Active: Sniffing on {interface} (Dry Run: {dry_run})")
    print("[*] Monitoring traffic baseline... Press Ctrl+C to exit.")
    
    packet_count = 0
    last_throttle = time.time()

    try:
        while True:
            try:
                raw_data, addr = sniffer.recvfrom(65535)
                packet_count += 1

                if packet_count > 200:
                    if time.time() - last_throttle < 1.0:
                        time.sleep(0.1)
                    packet_count = 0
                    last_throttle = time.time()

                ip_header = raw_data[:20]
                iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                src_ip = socket.inet_ntoa(iph[8])
                
                check_packet_against_active_rules(protocol="tcp", src_ip=src_ip, dst_port=80)

            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[*] Engine processing halted cleanly.")
    finally:
        sniffer.close()

if __name__ == "__main__":
    parser = argparse = argparse.ArgumentParser(description="mini_ids Engine Command-Line Utilities")
    parser.add_argument("--run", action="store_true", help="Launches the packet collection engine loop.")
    parser.add_argument("--list-rules", action="store_true", help="Queries the shared database.")
    parser.add_argument("--sync", type=str, metavar="FILEPATH", help="Ingests a text Suricata signatures file.")
    parser.add_argument("--toggle", nargs=3, metavar=("SID", "USER", "ACTION"), help="Toggles rule deployments.")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()

    if args.run:
        start_sniffer_engine()
    elif args.list_rules:
        list_tracked_rules()
    elif args.sync:
        sync_bulk_rules_file(args.sync)
    elif args.toggle:
        sid_target, user_target, action_target = args.toggle
        if action_target in ["apply", "remove"]:
            toggle_rule_deployment(sid_target, user_target, action_target)
        else:
            print("[-] Validation Error: Action parameter must be 'apply' or 'remove'.")
