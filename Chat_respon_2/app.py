from flask import Flask, render_template, request ,jsonify # Corrected import
import re

app = Flask(__name__)

# Define responses and keywords
responses = {
    'greet': 'Hello you! :)',
    'goodbye': 'Goodbye for now',
    'thankyou': 'You are very welcome',
    'default': 'Default message'
}

keywords = {
    'greet': ['hello', 'hi', 'hey'],
    'goodbye': ['bye', 'farewell'],
    'thankyou': ['thank', 'thx']
}

# Compile patterns
patterns = {intent: re.compile(r'\b(' + '|'.join(words) + r')\b') for intent, words in keywords.items()}

# Function to match intent
def match_intent(message):
    for intent, pattern in patterns.items():
        if pattern.search(message.lower()):  # Convert to lowercase for case-insensitive matching
            return intent
    return None

# Function to respond based on intent
def respond(message):
    intent = match_intent(message)
    return responses.get(intent, responses['default'])

@app.route('/')
def home():
    return render_template('index.html')  # Corrected function call

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_response = respond(user_message)
    return jsonify({'user_message': user_message, 'bot_response': bot_response})  # Added jsonify for JSON response

if __name__ == '__main__':
    app.run(debug=True)
