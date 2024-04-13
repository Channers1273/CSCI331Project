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
        try:
            return render_template("welcome.html", YOU=YOU, name=YOU.username, getAppImage=getAppImage)
        except Exception as e:
            print("Error in index():", e)
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
    if gameName in YOU.recentGames.keys():
        return render_template("game.html", gameName=gameName, gameID=gameID, getAppImage=getAppImage, YOU=YOU)
    else:
        return render_template("altGame.html", gameName=gameName, gameID=gameID, getAppImage=getAppImage, YOU=YOU)


@app.route("/gameList")
def gameList():
    return render_template("gameList.html", YOU=YOU)


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
            print("Error in login():", e)
            return render_template("login.html")
    else:
        return render_template("login.html")    

@app.route("/select", methods=["POST", "GET"])
def select():
    
    if request.method == "POST":
        game = request.form["game"]
        opponent = str(request.form["opp"])
        return redirect(url_for("compare", gameID=game, oppid=opponent))
    else:
        return render_template("gameSelection.html", YOU=YOU)

@app.route("/compare/<gameID>/<oppid>")
def compare(gameID, oppid):

    opp = friendUser(oppid)
    game = steam.apps.get_app_details(gameID)
    gamename = game[str(gameID)]['data']['name']
    imgLin = game[str(gameID)]['data']['header_image']
    yourAchievementData = getAchievementInfo(YOU.steamID, gameID)
    yourAchievements = {}

    for A in yourAchievementData:
        if yourAchievementData[A]['obtained'] == 1:
            yourAchievements[A] = yourAchievementData[A]

    oppAchievementData = getAchievementInfo(opp.steamID, gameID)

    oppAchievements = {}
    for A in oppAchievementData:
        if oppAchievementData[A]['obtained'] == 1:
            oppAchievements[A] = oppAchievementData[A]

    YNumAchievements = len(yourAchievements)
    ONumAchievements = len(oppAchievements)

    YRarestAchievement = getRarestAchievement(yourAchievements)
    ORarestAchievement = getRarestAchievement(oppAchievements)

    YRareAch = list(YRarestAchievement.keys())
    ORareAch = list(ORarestAchievement.keys())
    return render_template("gameComparison.html", YOU = YOU, opp = opp, gamename = gamename, image = imgLin, YA = YNumAchievements, OA = ONumAchievements, YRareAchievement = YRareAch, ORareAchievement = ORareAch, YRareAchievementRarity = yourAchievements, ORareAchievementRarity = oppAchievements)


@app.route("/user")
def user():
    return render_template("user.html", YOU=YOU)




if __name__ == '__main__':
    # debug is set to save rerun a server when change is made
    app.run(debug=True)
