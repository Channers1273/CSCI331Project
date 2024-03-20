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
        return render_template("welcome.html", YOU=YOU, name=YOU.username, getAppImage=getAppImage)
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
    # oppAchievements = { k:v for (k,v) in oppAchievementData if oppAchievementData[k]['obtained'] == 1}

    oppAchievements = {}
    for A in oppAchievementData:
        if oppAchievementData[A]['obtained'] == 1:
            oppAchievements[A] = oppAchievementData[A]

    YNumAchievements = len(yourAchievements)
    ONumAchievements = len(oppAchievements)

    # print('*' * 7)
    # print(yourAchievements) 
    # print('*' * 7)
    # print(oppAchievements) 

    '''
    for A in yourAchievements:
        if yourAchievements[A]['obtained'] == 1:
            YNumAchievements += 1

    for A in oppAchievements:
        if oppAchievements[A]['obtained'] == 1:
            ONumAchievements += 1
    '''

    YRarestAchievement = getRarestAchievement(yourAchievements)
    ORarestAchievement = getRarestAchievement(oppAchievements)

    YRareAch = YRarestAchievement.keys()
    print(YRareAch)
    ORareAch = ORarestAchievement.keys()
    print(ORareAch)
    # YRareAchRarity = YRarestAchievement[] 
    # ORareAchRarity = ORarestAchievement[]
    
    return render_template("gameComparison.html", YOU = YOU, opp = opp, gamename = gamename, image = imgLin, YA = YNumAchievements, OA = ONumAchievements)

if __name__ == '__main__':
    # print("Please enter your steam id")
    # id = JordanSteamID
    # YOU = SteamUser(id)

    # debug is set to save rerun a server when change is made
    app.run(debug=True)
