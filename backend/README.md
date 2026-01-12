# 🚀 PeerHop
### Gesture-Driven Local Sharing for Smart Campuses & Workspaces

PeerHop is a lightweight, system-tray based application that enables **touch-free, gesture-controlled sharing of text, files, and images** between devices connected on the same local network.

Built for **smart campuses, offices, labs, and collaborative environments**, PeerHop eliminates the friction of traditional sharing methods by combining **computer vision, local networking, and explicit user consent** — all without requiring internet access.

---

## 🎯 Vision & Purpose

In classrooms, libraries, and shared workspaces, quick data sharing often becomes unnecessarily complicated due to emails, pen drives, logins, or cloud uploads.

**PeerHop simplifies this experience.**

Using intuitive hand gestures and local peer discovery, users can instantly exchange content with nearby devices in a **fast, private, and natural way**.

### What PeerHop Solves
- ❌ No internet dependency  
- ❌ No sign-ups or pairing steps  
- ❌ No cloud storage or cables  
- ✅ Gesture-based, local, instant sharing  

---

## 🧠 Design Philosophy

PeerHop is built around **proximity-first collaboration**:

- Devices automatically discover peers on the same LAN  
- Transfers are triggered intentionally using gestures  
- Every data transfer requires explicit user approval  

This ensures **speed without compromising safety or privacy**.

---

## ⚙️ System Architecture & Approach

### Core Concepts
- Gesture recognition as the primary interaction method  
- Temporary local hosting for data transfer  
- Decentralized peer discovery over LAN  

### Technical Challenges Addressed
- Real-time hand gesture recognition  
- Zero-configuration peer discovery  
- Secure, consent-based file transfers  
- Low-overhead background execution  

### Key Innovations
- Hotkey-triggered webcam pipeline for gesture detection  
- Ephemeral FastAPI server launched only during transfers  
- UDP broadcasting for automatic peer discovery  
- Pop-up confirmation to prevent accidental sharing  

---

## 🛠️ Technology Stack

### Core Technologies

- **Programming Language:** Python 3.10  
- **UI / Tray Interface:** Tkinter  
- **Gesture Recognition:** MediaPipe + OpenCV  
- **Local Server:** FastAPI  
- **Networking:** UDP broadcasting over LAN  
- **Clipboard & File Handling:** Native OS utilities  

---

## ✨ Features

- ✋ **Gesture-based copy & paste**
  - ASL “3” → Copy data  
  - Open palm → Paste / receive data  

- ⌨️ **Hotkey controlled**
  - Activate via `Ctrl + M`  

- 🌐 **LAN-only operation**
  - Works completely offline  
  - No cloud or external servers  

- 🔐 **User-centric security**
  - Approval prompt before every transfer  
  - Temporary servers only during active sessions  

- 📂 **Multi-format support**
  - Text, files, images, screenshots  

- 🖥️ **Background execution**
  - Runs silently from the system tray  

---

## 📽️ Demo

🎥 **Demo Video:**  
https://youtu.be/jmeGnu144DU

---

## 🧪 Installation & Setup

### Prerequisites
- Python 3.10  
- pip  

### Dependencies
- TensorFlow  
- MediaPipe  
- OpenCV  
- FastAPI  
- Tkinter  

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/HarshitJain2103/PeerHop.git

# Navigate to the project directory
cd PeerHop

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
