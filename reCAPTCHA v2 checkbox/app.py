from flask import Flask, request, render_template_string, send_from_directory
import requests
import os

app = Flask(__name__)

RECAPTCHA_SECRET_KEY = "6LdOHpArAAAAAFghvE60W9_o4pUhG2ZM_kJgWfYR"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ✅ Serve static files like dog.jpg
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form.get('g-recaptcha-response')
    if not token:
        return "CAPTCHA failed. No token received.", 400

    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    })

    result = r.json()
    if result.get('success'):
        with open('index.html', 'r') as file:
            html = file.read()
        return render_template_string(html + '<script>document.getElementById("recaptcha-container").style.display="none";document.getElementById("content").style.display="block";</script>')
    else:
        return "CAPTCHA verification failed. Try again.", 403

if __name__ == '__main__':
    app.run(debug=True)
