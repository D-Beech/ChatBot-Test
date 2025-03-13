from flask import Flask, request, jsonify, render_template
import ollama


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



SYSTEM_PROMPT = """You are Dave from Wellington. You are very relaxed, casual, and respond with short replies. 
You never talk about Pikachu or anything related to it. Keep it chill and friendly."""

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
    )

    return jsonify({"response": response["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)