from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Replace with your actual Gemini API key
API_KEY = ""
FINE_TUNED_MODEL = "tunedModels/chatbottunedmodel-j9mu1tyhdkbn"  # Your fine-tuned model name
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"  # Corrected endpoint

def get_gemini_response(user_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"  # Add the API key in the Authorization header
    }
    data = {
        "contents": [{"parts": [{"text": user_message}]}],
    }

    try:
        response = requests.post(ENDPOINT.format(model_name=FINE_TUNED_MODEL), headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response generated.")
        else:
            print(f"Error: API responded with status code {response.status_code}")
            return "Sorry, I couldn't process your request. Please try again later."
    except Exception as e:
        print(f"Error while contacting Gemini API: {e}")
        return "Sorry, there was an error processing your request. Please try again later."

@app.route('/chat')
def serve_chatbot():
    return send_from_directory(app.static_folder, 'chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    print(f"Received message from user: {user_message}")  # Debugging
    bot_response = get_gemini_response(user_message)
    print(f"Bot response: {bot_response}")  # Debugging
    return jsonify({"response": bot_response})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
