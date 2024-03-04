from flask import Flask, redirect, render_template, url_for, request
from initialPythonFunctions import *

app = Flask(__name__)

# Initial YOU as None such that index() return login at first
YOU = None

@app.route("/")
def index():
    # when YOU exists (with input), render welcome.html
    # Error handling to be done for invalid Steam ID
    if YOU:
        return render_template("welcome.html", name=YOU.username)
    else:
        return redirect(url_for("login"))

@app.route("/friendsList")
def friendsList():
    flist = YOU.friendsList
    return render_template("friendsList.html", name=YOU.username, friends=flist)

@app.route("/login", methods=["POST", "GET"])
def login():
    # declare YOU as global variable for storing the input value
    global YOU

    # post method is set in login.html
    if request.method == "POST":
        user_id = request.form["sid"]
        YOU = SteamUser(user_id)
        return redirect(url_for("index"))
    else:
        return render_template("login.html")    

@app.route("/select", methods=["POST", "GET"])
def select():
    
    if request.method == "POST":
        game = request.form["game"]
        # gn = getAppName(game)
        opponent = str(request.form["opp"])
        # return redirect(url_for("compare", gameid = game, oppid = str(opponent)))
        return redirect(url_for("compare", gameID=game, oppid=opponent))
    else:
        return render_template("gameSelection.html")

@app.route("/compare/<gameID>/<oppid>")
def compare(gameID, oppid):

    opp = SteamUser(oppid)
    gamename = getAppName(gameID)
    imgLin = getAppImage(gameID)
    yourAchievements = getAchievementInfo(YOU.steamID, gameID)
    oppAchievements = getAchievementInfo(opp.steamID, gameID)
    YNumAchievements = 0
    ONumAchievements = 0

    for A in yourAchievements:
        if yourAchievements[A]['obtained'] == 1:
            YNumAchievements += 1

    for A in oppAchievements:
        if yourAchievements[A]['obtained'] == 1:
            ONumAchievements += 1
    
    return render_template("gameComparison.html", YOU = YOU, opp = opp, gamename = gamename, image = imgLin, YA = YNumAchievements, OA = ONumAchievements)

if __name__ == '__main__':
    # print("Please enter your steam id")
    # id = JordanSteamID
    # YOU = SteamUser(id)

    # debug is set to save rerun a server when change is made
    app.run(debug=True)
