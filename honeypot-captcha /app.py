from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Replace these with your actual keys
RECAPTCHA_SITE_KEY = '6LdOHpArAAAAAK3G9ppKQQn39w2iyPozHIWVXapO'
RECAPTCHA_SECRET_KEY = '6LdOHpArAAAAAFghvE60W9_o4pUhG2ZM_kJgWfYR'

# Log suspicious activity
LOG_FILE = os.path.join('logs', 'suspicious.log')
os.makedirs('logs', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', site_key=RECAPTCHA_SITE_KEY)

@app.route('/submit', methods=['POST'])
def submit():
    # Honeypot check (bots may fill hidden field)
    honeypot = request.form.get('email') or request.form.get('hidden_email')
    if honeypot:
        log_suspicious("Honeypot field was filled by bot.")
        return "Bot detected. Access denied.", 403

    # reCAPTCHA verification
    recaptcha_response = request.form.get('g-recaptcha-response')
    if not recaptcha_response:
        log_suspicious("Missing reCAPTCHA response.")
        return "Captcha verification failed.", 403

    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }

    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    if not result.get('success'):
        log_suspicious("Failed reCAPTCHA verification.")
        return "Captcha verification failed.", 403

    # Passed all checks
    return redirect(url_for('dog_page'))

@app.route('/dog')
def dog_page():
    return render_template('dog.html')

def log_suspicious(reason):
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{datetime.now()}] Suspicious attempt: {reason}\n")

if __name__ == '__main__':
    app.run(debug=True)
