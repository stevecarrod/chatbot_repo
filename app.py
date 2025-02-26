from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Allowed topics or keywords
ALLOWED_TOPICS = ["company policy", "product info", "support hours"]

def is_allowed_prompt(prompt):
    return any(topic in prompt.lower() for topic in ALLOWED_TOPICS)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt")

    if not is_allowed_prompt(prompt):
        return jsonify({"response": "Sorry, I can only answer questions about company policy, product info, or support hours."})

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are a helpful assistant that only answers questions about {', '.join(ALLOWED_TOPICS)}. Question: {prompt}",
        max_tokens=150
    )

    return jsonify({"response": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
