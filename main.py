from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv("GOOGLE_API")  # Load API key from .env
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Mock conversation data
conversation = []

@app.route('/')
def index():
    """Render the main page with the chatbox."""
    return render_template('index.html', conversation=conversation)

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handle user messages and interact with Gemini API."""
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Send user message to Gemini API
        response = model.generate_content(user_message)
        bot_response = response.text

        # Add messages to the conversation
        conversation.append({'user': user_message, 'bot': bot_response})
        # Return the bot's response
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)