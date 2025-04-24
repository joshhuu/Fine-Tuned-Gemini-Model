from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini API key
API_KEY = ""
genai.configure(api_key=API_KEY)

# Load the fine-tuned model
model = genai.GenerativeModel(model_name="tunedModels/chatbottunedmodel-j9mu1tyhdkbn")

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Extract the user's message
        user_message = request.json.get("message", "")
        logging.info(f"Received message: {user_message}")
        
        if not user_message.strip():  # Handle empty message
            return jsonify({"error": "Message cannot be empty"}), 400

        # Generate response from the model
        result = model.generate_content(user_message)
        response = result.text
        logging.info(f"Model response: {response}")

        # Return the model's response
        return jsonify({"response": response})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
