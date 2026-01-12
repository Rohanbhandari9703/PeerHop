import os
import sys
import socket
from plyer import notification

def send_notification(title, message):
    try:
        # Get the absolute path to the icon, handling packaging properly
        if getattr(sys, 'frozen', False):  # If running as a PyInstaller package
            icon_path = os.path.join(sys._MEIPASS, "assets/logo.ico")
        else:
            icon_path = os.path.abspath("assets/logo.ico")  # For development/testing

        # Send the notification
        notification.notify(
            title=title,
            message=message,
            app_name="SnapShare",
            app_icon=icon_path,  # Ensure the path is correct
            timeout=3  # Duration in seconds
        )
    except Exception as e:
        print("Notification Error:", e)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip