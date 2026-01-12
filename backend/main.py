import tkinter as tk
import threading
import keyboard
import pyautogui
import pyperclip
import time
import win32clipboard
import win32con
import server
import requests
import sys
import os
import pystray  # New import
import subprocess  # Import subprocess for restarting the app
from PIL import ImageGrab, Image
from io import BytesIO
from utils import send_notification
from gesture import detect_gesture
from server import start_server
from broadcast_listener import listen_for_snap2script
from broadcast_sender import send_broadcast
from datetime import datetime
from plyer import notification
from server import stop_server
from broadcast_sender import stop_broadcast

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller compatibility). """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# Detect the gesture and update the label
def detect_and_display(label_result=None):
    detected_gesture = detect_gesture()
    if detected_gesture == "2 5":
        detected_gesture = "paste"
        send_notification("Gesture Detected:", "Paste")
        threading.Thread(target=listen_for_snap2script, daemon=True).start()
    elif detected_gesture == "3 3":
        detected_gesture = "copy"
        status = copy()
        send_notification("Copy Gesture Detected!", status)
        threading.Thread(target=start_server, daemon=True).start()
        time.sleep(1)
        threading.Thread(target=send_broadcast, daemon=True).start()

        if server.clipboard_store["type"] == "text":
            send_clipboard_to_server(server.clipboard_store["data"])  
        elif server.clipboard_store["type"] == "file":
            upload_file_to_server(server.clipboard_store["data"])
        elif server.clipboard_store["type"] == "image":
            upload_screenshot_to_server(server.get_ip())
    else:
        send_notification("Gesture Detected", f"Gesture: {detected_gesture}")
    if label_result:
        label_result.config(text=f"Detected Gesture: {detected_gesture}")

def send_clipboard_to_server(data):
    try:
        ip = server.get_ip()
        url = f"http://{ip}:8000/clipboard"
        payload = {"data": data}
        response = requests.post(url, json=payload)
        print("📤 Clipboard data sent to server:", response.json())
    except Exception as e:
        print("❌ Error sending clipboard to server:", e)

def upload_file_to_server(file_path):
    try:
        ip = server.get_ip()
        url = f"http://{ip}:8000/upload"
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
        print("📤 File uploaded to server:", response.json())
    except Exception as e:
        print("❌ Error uploading file:", e)

def upload_screenshot_to_server(server_ip):
    try:
        start = time.time()
        img = ImageGrab.grabclipboard()
        if img is None:
            print("❌ No image in clipboard to upload.")
            return
        img = img.resize((img.width // 2, img.height // 2))
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        files = {
            'file': (f"screenshot_{timestamp}.jpg", buffer, 'image/jpeg')
        }
        response = requests.post(f"http://{server_ip}:8000/upload", files=files)
        if response.status_code == 200:
            print("✅ Screenshot uploaded to server successfully.")
        else:
            print(f"❌ Failed to upload screenshot. Status: {response.status_code}")
        print(f"⏱️ Total time: {round(time.time() - start, 2)} seconds")
    except Exception as e:
        print(f"🚨 Error uploading screenshot: {e}")

def listen_for_hotkey(label_result=None):
    while True:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('m'):
            send_notification("SnapShare","Dectecting Gesture...")
            detect_and_display(label_result)
            time.sleep(1)  # debounce

def screenshot_to_clipboard():
    try:
        img = ImageGrab.grab()
        time.sleep(0.2)
        output = BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("Screenshot copied to clipboard.")
        server.clipboard_store["type"] = "image"
        server.clipboard_store["data"] = "Screenshot in clipboard (image data not transferred here)"
        return "Screenshot Copied!"
    except Exception as e:
        print("Clipboard error during screenshot:", e)
        try: win32clipboard.CloseClipboard()
        except: pass
        return "Screenshot copy failed."

def copy():
    pyperclip.copy("")  
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    copied_text = pyperclip.paste().strip()
    if copied_text:
        server.clipboard_store["type"] = "text"
        server.clipboard_store["data"] = copied_text
        return "Selected text copied!"

    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            files = win32clipboard.GetClipboardData(win32con.CF_HDROP)
            if files:
                server.clipboard_store["type"] = "file"
                server.clipboard_store["data"] = files[0]
                return f"File copied: {files[0]}"
    except Exception as e:
        print("Error checking file clipboard:", e)
    finally:
        try: win32clipboard.CloseClipboard()
        except: pass

    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.4)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    copied_text = pyperclip.paste().strip()
    if copied_text:
        server.clipboard_store["type"] = "text"
        server.clipboard_store["data"] = copied_text
        return "Copied all text!"
    return screenshot_to_clipboard()

# Tray App Integration
def create_tray(root):
    def on_quit(icon, item):
        send_notification("SnapShare:","Closing App!")
        time.sleep(3)
        icon.stop()
        root.quit()
        os._exit(0)

    def restart_app(icon, item):
        print("Stopping Broadcast!")
        stop_broadcast()
        print("Stopping Server!")
        stop_server()
        try:
            sys.exit()  # Close the current app
        except SystemExit:
            pass
        subprocess.Popen([sys.executable, "main.py"])  # Restart the app

    def show_window(icon, item):
        root.after(0, root.deiconify)

    icon_path = resource_path("assets/logo.ico")
    icon_image = Image.open(icon_path).resize((64, 64))
    icon = pystray.Icon("SnapShare", icon_image, "SnapShare", menu=pystray.Menu(
        pystray.MenuItem("Show", show_window),
        pystray.MenuItem("Restart", restart_app),  # Add Restart option
        pystray.MenuItem("Quit", on_quit)
    ))

    threading.Thread(target=icon.run, daemon=True).start()

# Main App
def main():
    root = tk.Tk()
    root.title("SnapShare")
    root.geometry("400x200")
    root.configure(bg="#1e1e2f")  # Modern dark background
    root.protocol("WM_DELETE_WINDOW", lambda: root.withdraw())
    root.withdraw()  # Hide the window on startup

    # Modern styled label for gesture result
    label_result = tk.Label(
        root,
        text="Detected Gesture:",
        font=("Segoe UI", 16, "bold"),
        bg="#1e1e2f",
        fg="white"
    )
    label_result.pack(pady=(30, 10))

    # Instruction label
    instruction_label = tk.Label(
        root,
        text="Press Ctrl+M to detect gesture",
        font=("Segoe UI", 12),
        bg="#1e1e2f",
        fg="#cccccc"
    )
    instruction_label.pack()

    # Start hotkey listener
    threading.Thread(target=listen_for_hotkey, args=(label_result,), daemon=True).start()

    # Start tray icon
    create_tray(root)

    root.mainloop()

if __name__ == "__main__":
    main()
