    import os
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    import requests
    import logging

    app = Flask(__name__, static_folder='static')
    CORS(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Configuration
    API_KEY = os.environ.get('GEMINI_API_KEY', '')
    FINE_TUNED_MODEL = "tunedModels/chatbottunedmodel-j9mu1tyhdkbn"
    ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{FINE_TUNED_MODEL}:generateContent"

    def get_gemini_response(user_message):
        """
        Get response from Gemini API with improved error handling
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        try:
            # Timeout added to prevent hanging
            response = requests.post(
                ENDPOINT, 
                headers=headers, 
                json=data, 
                timeout=10
            )
            
            # Detailed error logging
            if response.status_code != 200:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return f"Error processing request. Status code: {response.status_code}"

            # Robust response parsing
            response_data = response.json()
            
            # Multiple levels of fallback for extracting text
            try:
                bot_response = (
                    response_data
                    .get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "No response generated.")
                )
            except (IndexError, KeyError) as parse_error:
                logger.error(f"Response parsing error: {parse_error}")
                bot_response = "Sorry, I couldn't parse the response correctly."

            return bot_response

        except requests.RequestException as req_error:
            logger.error(f"Request error: {req_error}")
            return "Network error occurred. Please check your connection."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."

    @app.route('/chat')
    def serve_chatbot():
        return send_from_directory(app.static_folder, 'chatbot.html')

    @app.route('/get_response', methods=['POST'])
    def get_response():
        """Handle chat response with input validation"""
        try:
            user_message = request.json.get("message", "").strip()
            
            if not user_message:
                return jsonify({"response": "Please enter a valid message."})

            logger.info(f"Received message: {user_message}")
            bot_response = get_gemini_response(user_message)
            logger.info(f"Bot response generated: {bot_response}")
            
            return jsonify({"response": bot_response})
        
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return jsonify({"response": "An error occurred processing your request."})

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/<path:filename>')
    def serve_static_files(filename):
        return send_from_directory(app.static_folder, filename)

    if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=5000)