from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Keep latest meeting link
MEETING_LINK = None

@app.route("/")
def home():
    return "✅ NIA Bot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    global MEETING_LINK
    data = request.get_json()
    user_message = data.get("message", "")

    context = f"""
    Meeting link (if available): {MEETING_LINK}
    User message: {user_message}
    """
    response = model.generate_content(context)

    return jsonify({"reply": response.text})

@app.route("/meeting", methods=["POST"])
def meeting():
    global MEETING_LINK
    data = request.get_json()
    MEETING_LINK = data.get("link")
    if not MEETING_LINK:
        return jsonify({"error": "No meeting link provided"}), 400
    return jsonify({"status": "ok", "meeting_link": MEETING_LINK})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
