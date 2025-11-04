from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.form.get('slider_verified') == 'true':
        return redirect(url_for('dog_page'))
    return "Verification failed", 403

@app.route('/dog')
def dog_page():
    return render_template('dog.html')

if __name__ == '__main__':
    app.run(debug=True)
