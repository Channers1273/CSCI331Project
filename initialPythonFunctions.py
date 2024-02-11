from steam import Steam
from decouple import config
import requests
import json


KyleSteamID = "76561198199245639"
JordanSteamID = "76561198208256371"

appIDTheFinals = 2073850
appIDGodOfWar = 1593500
appIDPalworld = 1623730
appIDLethalCompany = 1966720
appIDBlasphemous = 774361
appIDTheBindingOfIsaacRebirth = 250900

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

class SteamUser:

    def __init__(self, steamID: str):
        self.steamID = steamID
        self.username = self.getUsername() 
        self.friendsList = self.getFriends()
        self.recentGames = self.getRecentGames()
        self.achievements = {}

        '''
        for game in self.recentGames:
            apiGameAchievements = steam.apps.get_user_achievements(self.steamID, self.recentGames[game]['appid'])
            achievements = {}
            for achievement in apiGameAchievements['playerstats']['achievements']:
                displayName = getAchievementTitle(KEY, self.recentGames[game]['appid'], achievement['apiname'])
                apiname = achievement['apiname']
                rarity = getAchievementRarity(self.recentGames[game]['appid'], apiname)
                # achievements[achievement[displayName]] = {'apiname': apiname, 'rarity': rarity}
                self.achievements[displayName] = {'apiname': apiname, 'rarity': rarity}
        '''

    def getUsername(self):
        user = steam.users.get_user_details(self.steamID)
        return user['player']['personaname']

    def getFriends(self):

        friendsList = steam.users.get_user_friends_list(self.steamID)
        friends = {}
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
            recentGames[name] = {'appid': game['appid'], 'playtime': float(game['playtime_forever']/60)}
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


def getAchievementInfo(steamID: str, appid: int):
    apiGameAchievements = steam.apps.get_user_achievements(steamID, appid)
    achievementDict = {}
    for achievement in apiGameAchievements['playerstats']['achievements']:
        # print(achievement)
        apiname = achievement['apiname']
        displayName = getAchievementTitle(KEY, appid, apiname)
        achievementRarity = getAchievementRarity(appid, apiname)
        obtainStatus = achievement['achieved']
        # print(displayName)
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
    test = steam.apps.get_app_details(appid)
    print(test)

if __name__ == '__main__':
    user = SteamUser(JordanSteamID) 
    # user.listRecentGames()
    testInfo = getAchievementInfo(user.steamID, appIDBlasphemous)
    for k,v in testInfo.items():
        print(k,v)
