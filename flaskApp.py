from flask import Flask, redirect, render_template, url_for
from initialPythonFunctions import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("welcome.html", name=YOU.username)

@app.route("/friendsList")
def friendsList():
    flist = YOU.friendsList
    return render_template("friendsList.html", name=YOU.username, friends=flist)




@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == '__main__':
    print("Please enter your steam id")
    id = JordanSteamID
    YOU = SteamUser(id)


    app.run()
