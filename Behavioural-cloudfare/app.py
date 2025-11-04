from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

SITE_KEY = "0x4AAAAAABmzd_44Gb9ZtrcX"
SECRET_KEY = "0x4AAAAAABmzd2FoFTz1meBw81eUYLkbggk"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get('cf-turnstile-response')
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                'secret': SECRET_KEY,
                'response': token
            }
        )
        if resp.json().get("success"):
            return redirect("/dog")
        else:
            return "Failed CAPTCHA. Try again.", 400
    return render_template("index.html", site_key=SITE_KEY)

@app.route("/dog")
def dog_page():
    return render_template("dog.html")

if __name__ == "__main__":
    app.run(debug=True)
