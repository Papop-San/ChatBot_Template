from flask import Flask, request, jsonify, render_template
import random
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

rules = {
    'do you think (.*)': [
        'If {0}? Absolutely.',
        'No chance.'
    ],
    'do you remember (.*)': [
        'Did you think I would forget {0}?',
        "Why haven't you been able to forget {0}?",
        'What about {0}?',
        'Yes .. and?'
    ],
    'I want (.*)': [
        'What would it mean if you got {0}?',
        'Why do you want {0}?',
        "What's stopping you from getting {0}?"
    ],
    'if (.*)': [
        "Do you really think it's likely that {0}?",
        'Do you wish that {0}?',
        'What do you think about {0}?',
        'Really--if {0}!'
    ]
}

def match_rule(rules, message):
    response, phrase = "default", None
    for pattern, responses in rules.items():
        match = re.match(pattern, message)
        if match:
            response = random.choice(responses)
            if "{0}" in response:
                phrase = match.group(1)
    return response, phrase  

def replace_pronouns(message):
    message = message.lower()
    if 'me' in message:
        message = message.replace('me', 'you')
    if 'my' in message:
        message = message.replace('my', 'your')
    if 'your' in message:
        message = message.replace('your', 'my')
    if 'you' in message:
        message = message.replace('you', 'me')
    return message

def respond(message):
    response, phrase = match_rule(rules, message)
    if '{0}' in response and phrase:
        phrase = replace_pronouns(phrase)
        response = response.format(phrase)
    return response

@app.route('/api/message', methods=['POST'])
def api_message():
    user_message = request.json.get('message', '')
    bot_response = respond(user_message)
    return jsonify({'response': bot_response})

@app.route('/api/sentiment', methods=['POST'])
def api_sentiment():
    user_message = request.json.get('message', '')
    sentiment_scores = sid.polarity_scores(user_message)
    return jsonify(sentiment_scores)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
