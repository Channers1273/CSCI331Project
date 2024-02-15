from flask import Flask, redirect, render_template, url_for
from initialPythonFunctions import SteamUser

app = Flask(__name__)
@app.route("/")
def home():
    name = YOU.username
    return f"Welcome {name}"




if __name__ == '__main__':
    print("Please enter your steam id")
    id = int(input())
    YOU = SteamUser(id)


    app.run()
