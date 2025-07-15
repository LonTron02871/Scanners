#Simple Port Scanner with a GUI for simplicity

import socket
import threading
from datetime import datetime

# === Configuration ===
SCAN_TIMEOUT = 1  # seconds
LOG_FILE = "port_scan.log"


def log_to_file(message: str):
    """Append log messages to a file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")


def scan_port(host: str, port: int, gui_log_callback):
    """Scans a single port and reports status."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(SCAN_TIMEOUT)
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                message = f"[+] Port {port} is OPEN on {host}"
            else:
                message = f"[-] Port {port} is CLOSED on {host}"
        except socket.error as e:
            message = f"[!] Error scanning port {port} on {host}: {e}"

    # Log to GUI and file
    gui_log_callback(message)
    log_to_file(message)


def start_port_scan(host: str, start_port: int, end_port: int, gui_log_callback):
    """Starts scanning a range of ports."""
    gui_log_callback(f"[*] Starting scan on {host} from port {start_port} to {end_port}...")
    log_to_file(f"[*] Starting scan on {host} from port {start_port} to {end_port}...")

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(host, port, gui_log_callback))
        thread.daemon = True
        thread.start()


import tkinter as tk
from port_scanner import start_port_scan  # Assuming the module above is in `port_scanner.py`


def gui_log(message):
    log_text.insert(tk.END, message + '\n')
    log_text.see(tk.END)


def on_scan_click():
    host = entry_host.get()
    try:
        start_port = int(entry_start_port.get())
        end_port = int(entry_end_port.get())
    except ValueError:
        gui_log("[!] Invalid port range.")
        return

    start_port_scan(host, start_port, end_port, gui_log)


# --- Tkinter GUI ---
root = tk.Tk()
root.title("SIEM Port Scanner")

tk.Label(root, text="Target Host:").grid(row=0, column=0)
entry_host = tk.Entry(root)
entry_host.grid(row=0, column=1)

tk.Label(root, text="Start Port:").grid(row=1, column=0)
entry_start_port = tk.Entry(root)
entry_start_port.grid(row=1, column=1)

tk.Label(root, text="End Port:").grid(row=2, column=0)
entry_end_port = tk.Entry(root)
entry_end_port.grid(row=2, column=1)

tk.Button(root, text="Start Scan", command=on_scan_click).grid(row=3, column=0, columnspan=2, pady=10)

log_text = tk.Text(root, height=20, width=70)
log_text.grid(row=4, column=0, columnspan=2)

root.mainloop()
