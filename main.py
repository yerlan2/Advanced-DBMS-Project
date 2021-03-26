from flask import Flask, request, session, render_template, redirect, url_for, make_response, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main/home.html")


@app.route('/signup')
def signup():
    return render_template("auth/signup.html")


if __name__=="__main__":
    app.run(debug=True)
