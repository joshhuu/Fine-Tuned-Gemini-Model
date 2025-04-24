from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import logging
import speech_recognition as sr
from pydub import AudioSegment
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini API key
API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)

# Load the fine-tuned model
model = genai.GenerativeModel(model_name="tunedModels/chatbottunedmodel-j9mu1tyhdkbn")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to convert any audio file to WAV
def convert_to_wav(audio_file):
    try:
        # Load the audio file using pydub
        audio = AudioSegment.from_file(audio_file)
        wav_path = "user_audio.wav"
        audio.export(wav_path, format="wav")  # Export as WAV format
        logging.info("Audio file converted to WAV successfully.")
        return wav_path
    except Exception as e:
        logging.error(f"Error converting audio file to WAV: {str(e)}")
        return None

# Function to convert speech to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        logging.info(f"Speech-to-text successful: {text}")
        return text
    except sr.UnknownValueError:
        logging.error("Google Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        logging.error(f"Speech-to-text API error: {e}")
        return None

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Check if the request contains audio
        if 'audio' in request.files:
            audio_file = request.files['audio']
            # Save the uploaded audio file
            audio_path = 'user_audio'
            audio_file.save(audio_path)
            logging.info("Audio file received and saved.")
            
            # Convert the audio file to WAV
            wav_path = convert_to_wav(audio_path)
            if not wav_path:
                return jsonify({"error": "Audio file conversion failed"}), 500
            
            # Convert the audio to text
            user_message = speech_to_text(wav_path)
            if not user_message:
                return jsonify({"error": "Unable to transcribe speech"}), 400
            logging.info(f"Received user message: {user_message}")
        else:
            return jsonify({"error": "No audio file provided"}), 400
        
        # Check if the message is empty
        if not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Generate a response from the model
        try:
            result = model.generate_content(user_message)
            response = result.text
        except Exception as e:
            logging.error(f"Model generation failed: {str(e)}")
            return jsonify({"error": "Failed to generate response from the model"}), 500
        logging.info(f"Model response: {response}")

        # Return the model's response as text
        return jsonify({"response": response}), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
