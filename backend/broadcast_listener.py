import socket
import time
import requests
import pyperclip
import os
import tkinter as tk
import sys
from utils import send_notification
from pathlib import Path
from plyer import notification
from tkinter import ttk
BROADCAST_PORT = 54545
TIMEOUT = 6  #Seconds

def confirm_paste_to_user_a(user_a_ip):
    try:
        response = requests.post(f"http://{user_a_ip}:8000/paste-success", json={"message": f"{os.getlogin()} successfully pasted the data."})
        if response.status_code == 200:
            print("User A has been notified of the successful paste.")
        else:
            print("Failed to notify User A.")
    except Exception as e:
        print(f"Error sending notification to User A: {e}")

def fetch_clipboard_from_server(server_ip):
    try:
        pyperclip.copy("")  # Clear local clipboard
        response = requests.get(f"http://{server_ip}:8000/clipboard?username={os.getlogin()}", stream=True)

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = response.json()
                if data.get("type") == "text":
                    clipboard_content = data["data"]
                    pyperclip.copy(clipboard_content)
                    print(f"📋 Clipboard copied from server: {clipboard_content}")
                    send_notification("SnapShare", "📋 Text pasted from remote clipboard.")
                    confirm_paste_to_user_a(server_ip)
                else:
                    print("⚠️ Received JSON, but not text data.")

            elif "application/octet-stream" in content_type:

                # Safely get the desktop path on Windows
                desktop_path = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
                download_folder = desktop_path / "SnapShareDownloads"
                download_folder.mkdir(parents=True, exist_ok=True)

                # Try to extract filename from response headers
                content_disposition = response.headers.get("content-disposition", "")
                filename = "clipboard_file"  # default fallback
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[-1].strip().strip('"')

                filepath = download_folder / filename

                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"📁 File received and saved at: {filepath}")
                send_notification("SnapShare", f"📁 File saved: {filename}")
                confirm_paste_to_user_a(server_ip)
                
            else:
                print("Unknown content type received.")

        elif response.status_code == 403:
            send_notification("Failed to paste!", "Access Denied!")
        else:
            print(f"Failed to fetch clipboard. Status: {response.status_code}")

    except Exception as e:
        print(f"Error fetching clipboard: {e}")

    print("🛑 Closing the app...")
    return

def handle_connection(ip):
    print(f"🟢 Attempting to connect to the SnapShare server at {ip}...")
    fetch_clipboard_from_server(ip)

#Selection popup
def show_server_popup(servers):
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("SnapShare - Select User")
    root.geometry("400x350")
    root.eval('tk::PlaceWindow . center')
    root.attributes('-topmost', True)
    root.configure(bg="#1e1e2f")  # Dark modern background

    style = ttk.Style()
    style.theme_use("clam")

    # Style for user selection buttons
    style.configure("User.TButton",
                    font=("Segoe UI", 11),
                    padding=8,
                    background="#2d2d44",
                    foreground="white",
                    anchor="w",
                    relief="flat",
                    borderwidth=0)

    style.map("User.TButton",
              background=[("active", "#3b3b5c")])

    # Enhanced Style for selected button
    style.configure("Selected.User.TButton",
                    background="#4a90e2",       # brighter blue
                    foreground="white",
                    font=("Segoe UI", 11, "bold"),
                    anchor="w",
                    relief="solid",             # give border
                    bordercolor="#ffffff",
                    borderwidth=2,
                    padding=8)

    style.map("Selected.User.TButton",
              background=[("active", "#3a78c2")])

    # Style for connect button
    style.configure("Connect.TButton",
                    font=("Segoe UI", 11, "bold"),
                    padding=10,
                    background="#4a90e2",
                    foreground="white",
                    relief="flat")
    style.map("Connect.TButton",
              background=[("active", "#357ABD")])

    var = tk.StringVar(value="")  # No default selection

    # Title label
    tk.Label(root,
             text="Who do you want to receive data from?",
             font=("Segoe UI", 13, "bold"),
             bg="#1e1e2f",
             fg="white",
             anchor="w").pack(pady=(20, 10), padx=20, anchor="w")

    # Container for server list (left-aligned)
    button_container = tk.Frame(root, bg="#1e1e2f")
    button_container.pack(fill="x", padx=20, anchor="w")

    button_refs = {}  # Store references to buttons by IP

    def select(ip, btn):
        if var.get() == ip:
            var.set("")
            btn.configure(style="User.TButton")
        else:
            var.set(ip)
            for b in button_refs.values():
                b.configure(style="User.TButton")
            btn.configure(style="Selected.User.TButton")

    # Render each user as a button
    for server in servers:
        btn = ttk.Button(button_container,
                         text=server["username"],
                         style="User.TButton")
        btn.pack(fill="x", pady=5)
        btn.configure(command=lambda ip=server["ip"], b=btn: select(ip, b))
        button_refs[server["ip"]] = btn

    # Connect button (centered)
    ttk.Button(root, text="Connect", style="Connect.TButton", command=lambda: on_confirm()).pack(pady=25)

    def on_confirm():
        root.selected_ip = var.get() or servers[0]["ip"]
        root.destroy()

    root.mainloop()
    return getattr(root, "selected_ip", None)

def listen_for_snap2script():
    servers = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", BROADCAST_PORT))
    sock.settimeout(2)
    print(f"🟢 Listening for SnapShare servers...")
    start_time = time.time()

    while (time.time() - start_time) < TIMEOUT:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()

            if message.startswith("Snap2Script::"):
                try:
                    _, ip, username = message.strip().split("::")
                    if not any(s["ip"] == ip for s in servers):
                        print(f"🟢 Found SnapShare server from {username}")
                        servers.append({"ip": ip, "username": username})
                except ValueError:
                    print("⚠️ Invalid broadcast message format.")

        except socket.timeout:
            continue

    sock.close()

    if servers:
        print(f"🟢 Found {len(servers)} server(s).")
        selected_ip = show_server_popup(servers)
        if selected_ip:
            handle_connection(selected_ip)
    else:
        print("No servers found.")
        send_notification("SnapShare", "Noone is there to connect!")
        print("Closing the app!")
        return