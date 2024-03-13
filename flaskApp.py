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
        # rgames = YOU.listRecentGames
        try:
            return render_template("welcome.html", YOU=YOU, name=YOU.username, getAppImage=getAppImage)
        except Exception as e:
            print("Error:", e)
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/friendsList")
def friendsList():
    flist = YOU.friendsList
    return render_template("friendsList.html", name=YOU.username, friends=flist, YOU=YOU)

@app.route("/friend/ID=<friendID>")
def friend(friendID):
    FRIEND = friendUser(friendID)
    return render_template("friend.html", FRIEND=FRIEND, getAppImage=getAppImage, YOU=YOU)

@app.route("/game/name=<gameName>ID=<gameID>")
def game(gameID, gameName):
    return render_template("game.html", gameName=gameName, gameID=gameID, getAppImage=getAppImage, YOU=YOU)


@app.route("/login", methods=["POST", "GET"])
def login():
    # declare YOU as global variable for storing the input value
    global YOU

    # post method is set in login.html
    if request.method == "POST":
        user_id = request.form["sid"]
        try:
            YOU = SteamUser(user_id)
            return redirect(url_for("index"))
        except Exception as e:
            print("Error:", e)
            return render_template("login.html")
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
        return render_template("gameSelection.html", YOU=YOU)

@app.route("/compare/<gameID>/<oppid>")
def compare(gameID, oppid):

    opp = friendUser(oppid)
    game = steam.apps.get_app_details(gameID)
    gamename = game[str(gameID)]['data']['name']
    imgLin = game[str(gameID)]['data']['header_image']
    yourAchievements = getAchievementInfo(YOU.steamID, gameID)
    oppAchievements = getAchievementInfo(opp.steamID, gameID)
    YNumAchievements = 0
    ONumAchievements = 0

    for A in yourAchievements:
        if yourAchievements[A]['obtained'] == 1:
            YNumAchievements += 1

    for A in oppAchievements:
        if oppAchievements[A]['obtained'] == 1:
            ONumAchievements += 1
    
    return render_template("gameComparison.html", YOU = YOU, opp = opp, gamename = gamename, image = imgLin, YA = YNumAchievements, OA = ONumAchievements)

if __name__ == '__main__':
    # print("Please enter your steam id")
    # id = JordanSteamID
    # YOU = SteamUser(id)

    # debug is set to save rerun a server when change is made
    app.run(debug=True)
