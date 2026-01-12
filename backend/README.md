🚀 PeerHop
Gesture-Driven Local Sharing for Smart Campuses & Workspaces

PeerHop is a lightweight, system-tray based application that enables touch-free, gesture-controlled sharing of text, files, and images between devices connected to the same local network.

Designed for smart campuses, offices, labs, and hackathons, PeerHop removes the friction of traditional sharing methods by combining computer vision, local networking, and secure user approvals — all without requiring internet access.

🎯 Vision & Purpose

In classrooms, libraries, and collaborative workspaces, sharing small pieces of data often becomes unnecessarily complex — emails, pen drives, messaging apps, logins, and cloud uploads.

PeerHop rethinks this interaction.

By using simple hand gestures and local peer discovery, users can instantly exchange content with nearby devices in a fast, private, and intuitive way.

What PeerHop Solves

❌ No internet dependency

❌ No sign-ups or pairing steps

❌ No cloud storage or cables

✅ Just gestures + local network

🧠 Design Philosophy

PeerHop is built around proximity-based collaboration:

Devices discover each other automatically over LAN

Transfers are triggered intentionally via gestures

Every transfer requires explicit user approval

This ensures speed without sacrificing safety.

⚙️ System Approach
Core Ideas

Gesture recognition as the primary input mechanism

Temporary, on-demand local hosting for transfers

Decentralized peer discovery within the same network

Key Technical Challenges Addressed

Real-time and reliable hand gesture detection

Peer discovery without central servers

Secure, consent-based data transfer

Lightweight background execution (tray application)

Notable Innovations

Hotkey-activated webcam pipeline for gesture detection

Ephemeral FastAPI server spun up only during transfers

UDP-based broadcasting for zero-configuration peer discovery

Confirmation pop-ups to prevent accidental sharing

🛠️ Technology Stack
Core Components

UI / Tray Interface: Tkinter

Gesture Recognition: MediaPipe + OpenCV

Local Backend Server: FastAPI

Networking: UDP broadcasting over LAN

Clipboard & File Handling: Native OS utilities

Language: Python 3.10

✨ Features

✋ Gesture-based copy & paste

ASL “3” → Copy content

Open palm → Paste / receive content

⌨️ Hotkey controlled

Activate via Ctrl + M

🌐 Fully local

Works entirely over LAN

No internet required

🔐 User-first security

Approval prompt before every transfer

Temporary servers only during active sessions

📂 Multi-format support

Text, files, images, screenshots

🖥️ Always available

Runs silently in the system tray

📽️ Demo

🎥 Demo Video:
https://youtu.be/jmeGnu144DU

🧪 Installation & Setup
Prerequisites

Python 3.10

pip

Required Libraries

TensorFlow

MediaPipe

OpenCV

FastAPI

Tkinter

Setup Steps
# Clone the repository
git clone https://github.com/rohanbhandari9703/PeerHop.git

# Navigate into the project directory
cd PeerHop

# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py

📦 Data Handling Behavior

Text: Copied directly to the system clipboard

Files & Images: Saved to

PeerHopDownloads/


on the receiver’s machine

🔒 Privacy & Security Model

PeerHop is built with privacy by design:

Transfers occur only after sender approval

No persistent servers — everything is temporary

No external APIs or cloud storage involved

No data leaves the local network

🧬 Future Enhancements

📊 Smart Classroom Dashboard

View anonymized, non-sensitive usage statistics

🔐 Stronger Encryption Layer

For enterprise and institutional deployments

🌍 Cross-Platform Support

Linux and macOS compatibility

🧑‍💼 Admin Control Mode

Central enable/disable for lab or office machines

📎 Credits & Acknowledgements

MediaPipe by Google

FastAPI

OpenCV

All contributors and testers who helped refine PeerHop

📜 License

This project is released under a custom license.

❗ Commercial use, redistribution, or modification without explicit permission from the author is strictly prohibited.
Please refer to the full license file for detailed terms.

🏁 Closing Note

PeerHop was created to make human gestures a first-class input method for digital collaboration.
From classrooms to hackathons, it demonstrates how computer vision and local networking can come together to create faster, safer, and more natural interactions.