# logical captcha to type the word display over and then verify it

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/submit', methods=['POST'])
def submit():
    answer = request.form.get('captcha_answer', '').strip().lower()
    if answer == 'dog':
        return redirect(url_for('dog_page'))
    else:
        return render_template('index.html', error="Incorrect answer. Please try again!")

@app.route('/dog')
def dog_page():
    return render_template('dog.html')

if __name__ == '__main__':
    app.run(debug=True)
