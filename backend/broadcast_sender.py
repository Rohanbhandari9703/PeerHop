import socket
import time
import os
import keyboard
from server import stop_server
from utils import send_notification
BROADCAST_PORT = 54545
username = os.getlogin()
local_ip = socket.gethostbyname(socket.gethostname())
BROADCAST_MESSAGE = f"Snap2Script::{local_ip}::{username}"
BROADCAST_INTERVAL = 2
DURATION = 180
broadcast_running = False

def send_broadcast():
    global broadcast_running

    # Set the broadcast flag to True
    broadcast_running = True
    #Send a broadcast message to the local network indicating that Snap2Script is running.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    start_time = time.time() 
    
    print(f"🟢 Starting to send Snap2Script broadcast messages...")
    send_notification("To Stop Sending Data","Hold ctrl+k")
    while time.time() - start_time < DURATION:
        if not broadcast_running: # Stop if the broadcast should be stopped
            break
        if (keyboard.is_pressed('ctrl') and keyboard.is_pressed('k')):
            send_notification("SnapShare","Stopped Sending Data!")
            print("Forcefully stopping copy serving!")
            break
        if DURATION - 2 <= time.time() - start_time < DURATION:
            send_notification("SnapShare","Stopped sending data after 180 seconds")
        try:
            sock.sendto(BROADCAST_MESSAGE.encode(), ("<broadcast>", BROADCAST_PORT))
            print(f"🟢 Broadcast sent: {BROADCAST_MESSAGE} to port {BROADCAST_PORT}")
            time.sleep(BROADCAST_INTERVAL) 
            
        except Exception as e:
            print(f"Error while sending broadcast: {e}")
            break 
    
    sock.close()
    print(f"Stopped broadcasting after {DURATION} seconds.")
    print("Closing the Server!")
    stop_server()
    print("Closing the App!")
    return


def stop_broadcast():
    global broadcast_running
    broadcast_running = False  # Set flag to False to stop the broadcast
    print("Broadcast stopped.")

