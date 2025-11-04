from flask import Flask, request, send_from_directory, jsonify
import requests
import os

app = Flask(__name__)
RECAPTCHA_SECRET_KEY = '6LeHJJArAAAAAHF7MZL4izbWs5s4aduOYNnR9dic'  # replace with your real secret key

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/dog.jpeg')
def image():
    return send_from_directory('.', 'dog.jpg')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form.get('token')
    if not token:
        return jsonify({ "success": False, "message": "No token provided" })

    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token
        }
    )
    result = r.json()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
