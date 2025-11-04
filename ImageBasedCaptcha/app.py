from flask import Flask, render_template, request, jsonify, redirect, url_for
import random

app = Flask(__name__)

# Image metadata
images = [
    {"label": "dog", "filename": "dog.jpg"},
    {"label": "cat", "filename": "cat.jpeg"},
    {"label": "bird", "filename": "bird.jpeg"},
    {"label": "horse", "filename": "horse.jpeg"}
]

@app.route('/')
def index():
    selected = random.sample(images, 3)
    correct = random.choice(selected)
    return render_template('index.html', images=selected, prompt=correct["label"], answer=correct["filename"])

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    clicked = data.get('selected')
    correct = data.get('answer')
    if clicked == correct:
        return jsonify({"success": True, "redirect": url_for('dog_page')})
    return jsonify({"success": False})

@app.route('/dog')
def dog_page():
    return render_template('dog.html')

if __name__ == '__main__':
    app.run(debug=True)
