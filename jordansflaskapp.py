from flask import Flask, redirect, render_template, url_for
from initialPythonFunctions import SteamUser

app = Flask(__name__)


@app.route("/")
def index():
    name = YOU.username
    return f"Welcome {name}"

@app.route("/friendsList")
def friendsList():
    flist = YOU.friendsList
    return render_template("friendsList.html", name=YOU.username, friends=flist)




if __name__ == '__main__':
    print("Please enter your steam id")
    id = int(input())
    YOU = SteamUser(id)


    app.run()
