from flask import Flask, request, jsonify, render_template
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

LLAMA_SERVER_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """you are Goku, informal, short with responses, enthusiastic"""

MEMORY_FILE = "chat_memory.json"




# In-memory dictionary to store user and assistant messages
memory = {}

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    user_id = request.json.get("user_id", "default")  # Optionally use user ID to separate memory for different users

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Initialize user memory if it doesn't exist
    if user_id not in memory:
        memory[user_id] = []

    # Add the user message to memory
    memory[user_id].append({"role": "user", "content": user_message})

    # Prepare payload with history
    payload = {
        "model": "llama3.2",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + memory[user_id],
        "stream": False
    }

    try:
        response = requests.post(LLAMA_SERVER_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        # Get model's reply
        model_reply = data.get("message", {}).get("content", "No response from model.")

        # Add the assistant's reply to memory
        memory[user_id].append({"role": "assistant", "content": model_reply})

        return jsonify({"response": model_reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

    # user_message = request.json.get("message", "")

    # if not user_message:
    #     return jsonify({"error": "Message is required"}), 400

    # payload = {
    #     "model": "llama3.2",
    #     "messages": [
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": user_message},
    #     ],
    #     "stream": False
    # }

    # try:
    #     response = requests.post(LLAMA_SERVER_URL, json=payload)
    #     response.raise_for_status()
    #     data = response.json()  # Get the entire response JSON

    #     # You may need to adjust this depending on the actual response structure.
    #     # For example, if the response is under "message" -> "content", change accordingly.
    #     message_content = data.get("message", {}).get("content", "No response from model.")
        
    #     print(message_content)  # Debug print to ensure response is what you expect
    #     return jsonify({"response": message_content})

    # except requests.exceptions.RequestException as e:
    #     return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)