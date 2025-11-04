from flask import Flask, request, send_from_directory
import requests

app = Flask(__name__)

RECAPTCHA_SECRET_KEY = '6LcCJ5ArAAAAAEcRox5lBJBSL9gg_P3K_emy-txC'  # Replace this with your secret key

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/dog.jpg')
def image():
    return send_from_directory('.', 'dog.jpg')

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form.get('g-recaptcha-response')
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token
        }
    )
    result = response.json()
    if result.get("success"):
        return '''
            <link rel="stylesheet" href="/style.css">
            <h2>Verification successful! 🐶</h2>
            <img src="/dog.jpg" alt="A happy dog">
        '''
    else:
        return '''
            <link rel="stylesheet" href="/style.css">
            <h2>Verification failed. Please try again.</h2>
            <a href="/">Go Back</a>
        '''

if __name__ == '__main__':
    app.run(debug=True)
