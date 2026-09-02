#!/usr/bin/env python3
import curses
import json
import os
import time

HISTORY_LOG = '/var/log/mini_ids/history.json'
CONFIG_PATH = '/etc/mini_ids/config.json'

def load_incidents():
    incidents = []
    if os.path.exists(HISTORY_LOG):
        with open(HISTORY_LOG, 'r') as f:
            for line in f:
                if line.strip():
                    incidents.append(json.loads(line))
    return incidents[-8:]

def read_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f).get("defense_mode", "ACTIVE SPOOFING")
    return "ACTIVE SPOOFING"

def write_config(mode):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"defense_mode": mode}, f)

def render_ui(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000)
    modes = ["ACTIVE SPOOFING", "PASSIVE TRACKING (IGNORE)", "PORT SHIFTING"]
    current_idx = modes.index(read_config())
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(1, 2, "=== MINI-IDS/IPS ACTIVE COMMAND CONSOLE ===", curses.A_BOLD)
        stdscr.addstr(2, 2, f"System Clock: {time.strftime('%H:%M:%S')} | Target Rules Pipeline: Connected")
        stdscr.addstr(4, 2, "Select Network Defensive Policy Mode:", curses.A_BOLD)
        for idx, mode in enumerate(modes):
            if idx == current_idx:
                stdscr.addstr(5 + idx, 4, f" => [X] {mode} ", curses.A_REVERSE)
            else:
                stdscr.addstr(5 + idx, 4, f"    [ ] {mode} ")
        stdscr.addstr(9, 2, "Controls: Use [UP/DOWN Arrow Keys] to switch modes. Press [Q] to close dashboard.")
        stdscr.addstr(11, 2, "Captured Attacker Identities Telemetry Stream:", curses.A_BOLD)
        stdscr.addstr(12, 2, f"{'Timestamp':<20} | {'Source IP':<15} | {'Hardware Canvas Sig':<20} | {'IP Churn/VPN?':<10}", curses.A_UNDERLINE)
        incidents = load_incidents()
        for offset, incident in enumerate(incidents):
            if 13 + offset >= h - 2:
                break
            stdscr.addstr(13 + offset, 2, f"{incident.get('timestamp',''):<20} | {incident.get('attacker_ip',''):<15} | {incident.get('hardware_fingerprint',''):<20} | {incident.get('anonymity_tool_active',''):<10}")
        stdscr.refresh()
        try:
            key = stdscr.getch()
            if key in [ord('q'), ord('Q')]:
                break
            elif key == curses.KEY_DOWN:
                current_idx = (current_idx + 1) % len(modes)
                write_config(modes[current_idx])
            elif key == curses.KEY_UP:
                current_idx = (current_idx - 1) % len(modes)
                write_config(modes[current_idx])
        except Exception:
            pass

if __name__ == '__main__':
    curses.wrapper(render_ui)
