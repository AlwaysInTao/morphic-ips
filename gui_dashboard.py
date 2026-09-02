import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
import os
import threading
import time

class IDSDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini-IDS/IPS Morphic Control Center")
        self.root.geometry("1200x750")
        self.root.configure(bg="#1e1e1e")

        # Style Configurations
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10, 'bold'), background='#2d2d2d', foreground='white')
        style.map('TButton', background=[('active', '#404040')])
        style.configure('TMenubutton', font=('Helvetica', 10, 'bold'), background='#007acc', foreground='white')

        # Left Control Sidebar Panel
        sidebar = tk.Frame(root, width=260, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        sidebar.pack(side="left", fill="y", padx=5, pady=5)

        title_label = tk.Label(sidebar, text="IDS/IPS MTD Engine", font=("Helvetica", 12, "bold"), fg="#00ff00", bg="#252526")
        title_label.pack(pady=15, padx=10)

        # Web Dashboard Hyperlink Panel
        web_frame = tk.Frame(sidebar, bg="#2d2d2d", padx=5, pady=5)
        web_frame.pack(fill="x", padx=15, pady=5)
        link_label = tk.Label(web_frame, text="Launch Web Admin Portal", font=("Helvetica", 10, "underline"), fg="#4dc3ff", bg="#2d2d2d", cursor="hand2")
        link_label.pack(pady=5)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("http://127.0.0.1:8080"))

        # Defense Mode Selection Header
        mode_label = tk.Label(sidebar, text="Active Defense Profile:", font=("Helvetica", 10, "bold"), fg="#aaaaaa", bg="#252526")
        mode_label.pack(anchor="w", padx=15, pady=(15, 2))

        # Operational Mode Dropdown Selector
        self.mode_var = tk.StringVar()
        self.mode_selector = ttk.Combobox(sidebar, textvariable=self.mode_var, state="readonly", font=("Helvetica", 10))
        self.mode_selector['values'] = ("Passive Tracking", "Active Spoofing", "Port Shifting")
        self.mode_selector.current(0)
        self.mode_selector.pack(fill="x", padx=15, pady=5)
        self.mode_selector.bind("<<ComboboxSelected>>", self.change_defense_mode)

        # Core Action Buttons Separator
        sep = ttk.Separator(sidebar, orient='horizontal')
        sep.pack(fill='x', padx=15, pady=15)

        btn_shift = ttk.Button(sidebar, text="Force Morphic Shift", command=self.trigger_shift)
        btn_shift.pack(fill="x", pady=6, padx=15)

        btn_reset = ttk.Button(sidebar, text="Reset Firewall Baseline", command=self.reset_firewall)
        btn_reset.pack(fill="x", pady=6, padx=15)

        btn_status = ttk.Button(sidebar, text="Check Engine Status", command=self.check_status)
        btn_status.pack(fill="x", pady=6, padx=15)

        # Right-Hand Workspace (Split Vertically between Terminal and Telemetry)
        right_workspace = tk.Frame(root, bg="#1e1e1e")
        right_workspace.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Upper Container: Interactive Terminal Interface
        term_container = tk.Frame(right_workspace, bg="#111111")
        term_container.pack(side="top", fill="both", expand=True, pady=(0, 5))
        tk.Label(term_container, text="Active System Execution Log Window", font=("Helvetica", 10, "bold"), fg="#aaaaaa", bg="#111111").pack(anchor="w", pady=3, padx=5)
        
        self.console_box = tk.Frame(term_container, bg="black")
        self.console_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Lower Container: Attacker Identity Telemetry Stream
        telemetry_container = tk.Frame(right_workspace, height=220, bg="#1e1e1e", highlightbackground="#333333", highlightthickness=1)
        telemetry_container.pack(side="bottom", fill="x", pady=(5, 0))
        tk.Label(telemetry_container, text="Captured Attacker Identity Telemetry Stream (IP Churn / Canvas Signatures)", font=("Helvetica", 10, "bold"), fg="#ff3333", bg="#1e1e1e").pack(anchor="w", pady=5, padx=5)

        # Scrolling Text Display for live telemetry parsing
        self.telemetry_text = tk.Text(telemetry_container, height=8, bg="#000000", fg="#ff9900", font=("Courier", 9), state="disabled")
        self.telemetry_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Force render UI elements to acquire the native X11 window window handle ID
        self.root.update()
        self.launch_embedded_terminal()
        
        # Start a secure background helper threat monitoring parser thread
        threading.Thread(target=self.stream_attacker_telemetry, daemon=True).start()

    def launch_embedded_terminal(self):
        wid = self.console_box.winfo_id()
        # Automate xterm to follow-stream engine actions live
        shell_cmd = "sudo journalctl -u mini-ids.service -f -n 20"
        cmd = [
            "xterm", "-into", str(wid), "-bg", "black", "-fg", "#00ff00",
            "-sb", "-geometry", "100x18", "-e", "bash", "-c", shell_cmd
        ]
        subprocess.Popen(cmd)

    def change_defense_mode(self, event):
        selected_mode = self.mode_var.get()
        print(f"[*] Operational Shift: Transitioning network context to [{selected_mode}] Profile...")
        # Direct hooks to update your backend states natively
        if selected_mode == "Active Spoofing":
            os.system("sudo systemctl restart mini-ids.service") # Placeholder execution logic
        elif selected_mode == "Port Shifting":
            pass

    def trigger_shift(self):
        print("[*] Triggering Polymorphic Network Shift Sequence...")
        os.system("sudo iptables -t mangle -A POSTROUTING -d 127.0.0.1 -p tcp -j TTL --ttl-set 128")

    def reset_firewall(self):
        print("[*] Executing Firewall Flush baseline...")
        os.system("/home/brian/mini_ids/flush.sh")

    def check_status(self):
        print("[*] Queries system service states...")
        os.system("systemctl status mini-ids.service --no-pager")

    def log_telemetry_message(self, message):
        self.telemetry_text.config(state="normal")
        self.telemetry_text.insert(tk.END, message + "\n")
        self.telemetry_text.see(tk.END)
        self.telemetry_text.config(state="disabled")

    def stream_attacker_telemetry(self):
        # Background task that polls files or feeds to print identity telemetry data dynamically
        time.sleep(2)
        self.log_telemetry_message("[*] Threat intel extraction thread operational. Awaiting client footprint signatures...")
        
        # Real-time parsing loop mockup (Integrates with engine.py logs)
        while True:
            try:
                if os.path.exists("/home/brian/mini_ids/ids_trigger.json"):
                    # Extract active churn stats or signatures when written
                    pass
            except Exception:
                pass
            time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = IDSDashboard(root)
    root.mainloop()
