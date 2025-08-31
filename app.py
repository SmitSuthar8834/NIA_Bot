from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import subprocess
import json
import threading
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Path for persistent meeting storage
STORE_FILE = "meeting_store.json"

def save_meeting_link(link: str):
    with open(STORE_FILE, "w") as f:
        json.dump({"meeting_link": link}, f)

def load_meeting_link():
    if not os.path.exists(STORE_FILE):
        return None
    with open(STORE_FILE, "r") as f:
        data = json.load(f)
        return data.get("meeting_link")

@app.route("/")
def home():
    return "✅ NIA Bot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    meeting_link = load_meeting_link()
    data = request.get_json()
    user_message = data.get("message", "")

    context = f"""
    Meeting link (if available): {meeting_link}
    User message: {user_message}
    """
    response = model.generate_content(context)

    return jsonify({"reply": response.text})

@app.route("/meeting", methods=["POST"])
def meeting():
    data = request.get_json()
    link = data.get("link")
    if not link:
        return jsonify({"error": "No meeting link provided"}), 400

    save_meeting_link(link)
    return jsonify({"status": "ok", "meeting_link": link})

@app.route("/n8n/webhook", methods=["POST"])
def n8n_webhook():
    """Endpoint for n8n to send meeting links"""
    data = request.get_json()
    meeting_link = data.get("meeting_link") or data.get("link") or data.get("url")
    
    if not meeting_link:
        return jsonify({"error": "No meeting link found in payload"}), 400
    
    save_meeting_link(meeting_link)
    
    # Log the meeting details
    event_title = data.get("event_title", "Unknown Meeting")
    event_start = data.get("event_start", "Unknown Time")
    
    print(f"📅 Meeting received: {event_title}")
    print(f"🕐 Start time: {event_start}")
    print(f"🔗 Meeting link: {meeting_link}")
    
    # Auto-join if enabled (cloud version - just log for now)
    auto_join = data.get("auto_join", False)
    if auto_join:
        print("🤖 Auto-join requested - Bot would join meeting in production")
        # In cloud deployment, we can't run the GUI bot, so we just acknowledge
        return jsonify({
            "status": "acknowledged", 
            "meeting_link": meeting_link,
            "message": "Meeting received and logged. Bot deployment successful!",
            "event_title": event_title,
            "event_start": event_start
        })
    
    return jsonify({"status": "saved", "meeting_link": meeting_link})

@app.route("/join_meeting", methods=["POST"])
def join_meeting():
    data = request.get_json()
    link = data.get("link") or load_meeting_link()
    enhanced = data.get("enhanced", True)  # Use enhanced bot by default
    
    if not link:
        return jsonify({"error": "No link available"}), 400

    try:
        bot_script = "enhanced_meet_bot.py" if enhanced else "nia_meet_bot.py"
        subprocess.Popen(["python", bot_script, link])
        return jsonify({"status": "joining", "link": link, "bot_type": "enhanced" if enhanced else "basic"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/status", methods=["GET"])
def status():
    """Health check and status endpoint"""
    meeting_link = load_meeting_link()
    return jsonify({
        "status": "running",
        "has_meeting_link": bool(meeting_link),
        "meeting_link": meeting_link if meeting_link else None,
        "endpoints": {
            "chat": "/chat",
            "meeting": "/meeting", 
            "join_meeting": "/join_meeting",
            "n8n_webhook": "/n8n/webhook",
            "status": "/status"
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
