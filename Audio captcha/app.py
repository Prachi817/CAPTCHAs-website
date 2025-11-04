from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import random
import string
import os
from gtts import gTTS
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"
AUDIO_FOLDER = "static"

def generate_random_code(length=5):
    return ''.join(random.choices(string.digits, k=length))

def generate_audio_captcha(code):
    filename = f"captcha_{int(time.time())}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    # Generate audio using Google TTS
    tts = gTTS(text="Please type the following numbers: " + " ".join(code), lang="en")
    tts.save(filepath)

    # Save the code in session
    session['captcha_code'] = code
    session['captcha_file'] = filename

@app.route('/')
def index():
    code = generate_random_code()
    generate_audio_captcha(code)
    return render_template('index.html', audio_file=session['captcha_file'])

@app.route('/retry')
def retry():
    code = generate_random_code()
    generate_audio_captcha(code)
    return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    slider_verified = request.form.get('slider_verification')
    audio_input = request.form.get('audio_captcha')
    captcha_code = session.get('captcha_code')

    if slider_verified == "unlocked" and audio_input == captcha_code:
        return redirect(url_for('dog_page'))
    return "Verification failed. Please try again.", 403

@app.route('/dog')
def dog_page():
    return render_template('dog.html')

if __name__ == '__main__':
    app.run(debug=True)
