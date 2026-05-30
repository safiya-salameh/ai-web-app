from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_ai():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please write a question first."
        }), 400

    if not API_KEY:
        return jsonify({
            "reply": "ERROR: GROQ_API_KEY is missing. Check your .env file."
        }), 500

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI study assistant for beginners. Explain clearly and simply."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        },
        timeout=30
    )

    data = response.json()

    print("Groq response:", data)

    if "choices" not in data:
        return jsonify({
            "reply": f"Groq API Error: {data}"
        }), 500

    ai_reply = data["choices"][0]["message"]["content"]

    return jsonify({
        "reply": ai_reply
    })


if __name__ == "__main__":
    app.run(debug=True)