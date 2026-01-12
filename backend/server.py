import uvicorn
import io
import asyncio
import tkinter as tk
from threading import Thread
from utils import send_notification,get_ip
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from tkinter import messagebox
from plyer import notification

app = FastAPI()

# Store the clipboard data (text or file)
clipboard_store = {
    "type": None,  # "text" or "file"
    "data": None,   # text data or file content in bytes
    "filename": None
}

#Clipboard Storage
class ClipboardData(BaseModel):
    data: str  # this will be for text data

#In-memory file storage
in_memory_files = {}

server_instance = None  # Reference to the server for shutdown

def run_uvicorn_server():
    global server_instance
    config = uvicorn.Config(app, host=get_ip(), port=8000, log_level="info")
    server_instance = uvicorn.Server(config)
    asyncio.run(server_instance.serve())

def start_server():
    print(f"🌐 Server running at http://{get_ip()}:8000")
    Thread(target=run_uvicorn_server, daemon=True).start()

def stop_server():
    global server_instance
    if server_instance and not server_instance.should_exit:
        print("🛑 Shutting down SnapShare server from broadcast_listener...")
        server_instance.should_exit = True

#Clipboard Approval Logic
def request_approval(username):
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        approved = messagebox.askyesno("Snap2Script Approval", f"Device at {username} wants to paste your clipboard.\nAllow access?")
        root.destroy()

        if approved:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Failed to show approval dialog: {e}")
        return False


#Endpoints...

@app.get("/")
def home_display():
    return {"message": "Server Started!♥"}

@app.get("/clipboard", responses={
    200: {
        "description": "Get clipboard data (text or file)",
        "content": {
            "application/json": {
                "example": {"type": "text", "data": "example text"}
            },
            "application/octet-stream": {
                "example": "File content streamed"
            }
        }
    }
})
def get_clipboard(username: str):
    # Ask for user A's approval before proceeding
    print(f"🟡 Incoming clipboard request from {username}")
    permssion = request_approval(username)
    if not permssion:
        print("Access denied by user.")
        raise HTTPException(status_code=403, detail="Access denied by user")

    # Proceed if access is approved
    if clipboard_store["type"] == "text":
        return JSONResponse(content={
            "type": "text",
            "data": clipboard_store["data"]
        })

    elif clipboard_store["type"] == "file" and clipboard_store["data"]:
        file_content = io.BytesIO(clipboard_store["data"])
        headers = {
            "Content-Disposition": f"attachment; filename={clipboard_store['filename']}"
        }
        return StreamingResponse(
            file_content,
            media_type="application/octet-stream",
            headers=headers
        )

    else:
        raise HTTPException(status_code=400, detail="No clipboard data available")
    
class PasteSuccess(BaseModel):
    message: str

@app.post("/paste-success")
async def paste_success(success: PasteSuccess):
    # User A gets notified of the successful paste
    send_notification("SnapShare", success.message)
    print(f"🟢 {success.message}")
    return {"status": "Notification sent to User A"}

@app.post("/clipboard")
async def receive_clipboard(data: ClipboardData):
    clipboard_store["type"] = "text"
    clipboard_store["data"] = data.model_dump().get("data")
    print(f"\n📥 Clipboard Received: {clipboard_store['data']}")
    return {"message": "Clipboard stored"}

# File upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    clipboard_store["type"] = "file"
    clipboard_store["data"] = content
    clipboard_store["filename"] = file.filename
    print(f"📥 File '{file.filename}' stored in memory. Size: {len(content)} bytes")
    return {"filename": file.filename, "message": "File uploaded and stored in memory"}
