from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "Jordan can't code without VSCode <h4>WHAT A GOOBER</h4>"

if __name__ == '__main__':
    app.run()
