from steam import Steam
from decouple import config
import requests
import json

# This is a comment made by Kyle
#This is Jordans second attempt at adding a comment
KyleSteamID = "76561198199245639" 
JordanSteamID = "76561198208256371"
AlvinSteamID = "76561198419880283"
OtherAlvinSteamID = "76561199028603569"
DylanSteamID = "76561198146107396"

appIDTheFinals = 2073850
appIDGodOfWar = 1593500
appIDPalworld = 1623730
appIDLethalCompany = 1966720
appIDBlasphemous = 774361
appIDTheBindingOfIsaacRebirth = 250900

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)                              #object that represents steam database

class SteamUser:

    def __init__(self, steamID: str):
        self.steamID = steamID
        self.username = self.getUsername() 
        self.friendsList = self.getFriends()
        self.recentGames = self.getRecentGames()
        self.achievements = {}
        self.avatar = self.getAvatar()

    def getUsername(self):
        user = steam.users.get_user_details(self.steamID)
        return user['player']['personaname']

    def getFriends(self):
        friendsList = steam.users.get_user_friends_list(self.steamID)
        friends = {}                            #dictionary of friends with usernames as keys, id's as elements
        for friend in friendsList['friends']:
            name = friend['personaname']
            friends[name] = friend['steamid']
        return friends

    def listFriends(self):
        for friend in self.friendsList:
            print(friend)

    def getRecentGames(self):
        apiGames = steam.users.get_user_recently_played_games(self.steamID)
        recentGames = {}
        for game in apiGames['games']:
            name = game['name']
            recentGames[name] = {'appid': game['appid'], 'playtime_forever': float(game['playtime_forever']/60), 'playtime_2weeks': float(game['playtime_2weeks']/60) }
        return recentGames

    def listRecentGames(self):
        for game in self.recentGames:
            print(game, "appid: " + str(self.recentGames[game]['appid']))

    def getOwnedGames(self):
        apiOwnedGames = steam.users.get_owned_games(self.steamID)
        print(apiOwnedGames)

    def getUserSteamLevel(self):
        steamLevel = steam.users.get_user_steam_level(self.steamID)
        return steamLevel['player_level']

    def listAchievement(self, displayName):
        for achievement in self.achievements[displayName]:
            print(achievement)

    def getAvatar(self):
        data = steam.users.get_user_details(self.steamID)
        return data['player']['avatar']


class friendUser:
    def __init__(self, id):
        self.steamID = id
        self.userDet = steam.users.get_user_details(self.steamID)
        self.avatar = self.userDet['player']['avatar']
        



def getAchievementInfo(steamID: str, appid: int):
    apiGameAchievements = steam.apps.get_user_achievements(steamID, appid)
    achievementDict = {}
    for achievement in apiGameAchievements['playerstats']['achievements']:
        apiname = achievement['apiname']
        displayName = getAchievementTitle(KEY, appid, apiname)
        achievementRarity = getAchievementRarity(appid, apiname)
        obtainStatus = achievement['achieved']
        achievementDict[displayName] = {'apiname': apiname, 'rarity': achievementRarity, 'obtained': obtainStatus}
    return achievementDict

def getAchievementTitle(apikey, appid, apiname) -> str:
    url = f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={apikey}&appid={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        achievements = data['game']['availableGameStats']['achievements']
        for achievement in achievements:
            if achievement['name'] == apiname:
                return achievement['displayName']
    return None

def getAchievementRarity(appid, apiname):
    url = f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        achievements = data['achievementpercentages']['achievements']
        for achievement in achievements:
            if achievement['name'] == apiname:
                return achievement['percent']
    return None

def describeGame(appid):
    test = steam.aapps.get_app_details(appid)
    print(test)


#gets the profile playtime for the last 2 weeks in minutes
def getGameTimeRecent(userid: int, appid: int):
        games = steam.users.get_user_recently_played_games(userid)['games']
        for g in games:
            if g['appid'] == appid:
                return g['playtime_2weeks']

#provided an appid returns the name of the game
def getAppName(appid: int) -> str:
    game = steam.apps.get_app_details(appid)
    return game[str(appid)]['data']['name'] 

def getAppImage(appid: int):
    image = steam.apps.get_app_details(appid)
    return image[str(appid)]['data']['header_image']

if __name__ == '__main__':

    user = steam.users.get_user_details(KyleSteamID)
    print(user)
    # user = SteamUser(DylanSteamID) 
    # user.listRecentGames()
    # print(getGameTimeRecent(user.steamID, appIDBlasphemous))
