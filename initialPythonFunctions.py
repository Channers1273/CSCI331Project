from steam import Steam
from decouple import config
import requests
import json
import random

# This is a comment made by Kyle
#This is Jordans second attempt at adding a comment
KyleSteamID = "76561198199245639" 
JordanSteamID = "76561198208256371"
AlvinSteamID = "76561198419880283"
OtherAlvinSteamID = "76561199028603569"
DylanSteamID = "76561198146107396"
englishID = "en"

appIDTheFinals = 2073850
appIDGodOfWar = 1593500
appIDPalworld = 1623730
appIDLethalCompany = 1966720 
appIDBlasphemous = 774361
appIDTheBindingOfIsaacRebirth = 250900
appIDWeWereHere = 582500

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)                              #object that represents steam database

class SteamUser:

    def __init__(self, steamID: str):
        user = steam.users.get_user_details(steamID)
        self.steamID = steamID
        self.username = user['player']['personaname']
        self.friendsList = self.getFriends()
        self.recentGames = self.getRecentGames()
        self.achievements = self.getRecentAchievements()
        self.avatar = user['player']['avatarfull']
        self.DDFriends = self.getDropdownFriends()      # should do the work of making an appropriately
                                                        # sized dict of friend name/id pairs just like friendsList
        self.DDGames = self.getDropdownGames()

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
        if 'games' in apiGames:
            for i, game in enumerate(apiGames['games']):
            # Limit to 5 games
                if i >= 5:
                    break
                name = game['name']
                recentGames[name] = {'appid': game['appid'], 'playtime_forever': float(game['playtime_forever']/60), 'playtime_2weeks': float(game['playtime_2weeks']/60) }
        return recentGames
        # original
        # for game in apiGames['games']:
        #     name = game['name']
        #     recentGames[name] = {'appid': game['appid'], 'playtime_forever': float(game['playtime_forever']/60), 'playtime_2weeks': float(game['playtime_2weeks']/60) }
        # return recentGames

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

    def getRecentAchievements(self):
        recentAchievements = {}
        # Limit to 1 recent games to save loading time (2 sometimes timeout...)
        # Comment out the for loop to enhance performance
        for game_name, game_info in list(self.recentGames.items())[:1]:
            appid = game_info['appid']
            # Fetch all recent achievements for the game before calling api
            all_achievements = getAchievementInfo(self.steamID, appid)
            # Limit to 5 recent achievements
            recentAchievements[game_name] = dict(list(all_achievements.items())[:5])
        return recentAchievements

    # Not really needed anymore
    def getAvatar(self):
        data = steam.users.get_user_details(self.steamID)
        return data['player']['avatar']
    
    def getDropdownFriends(self) -> dict:
        if not self.friendsList:
            return {}
        num = 5
        if len(self.friendsList) < 5:
            num = len(self.friendsList)
        temp = self.friendsList.copy()
        newDict = {}
        for x in range(num):
            element = random.choice(list(temp))
            if element not in [newDict.keys()]:
                newDict[element] = temp[element]
                temp.pop(element)
        return newDict
    
    def getDropdownGames(self) -> dict:
        if not self.recentGames:
            return {}
        num = 5
        if len(self.recentGames) < 5:
            num = len(self.recentGames)
        temp = self.recentGames.copy()
        newDict = {}
        for x in range(num):
            element = random.choice(list(temp))
            if element not in [newDict.keys()]:
                newDict[element] = temp[element]['appid']
                temp.pop(element)
        return newDict
                
                




class friendUser:
    def __init__(self, id):
        self.steamID = id
        self.userDet = steam.users.get_user_details(self.steamID)
        self.avatar = self.userDet['player']['avatarfull']
        self.username = self.userDet['player']['personaname']
        self.recentGames = self.getRecentGames()


    def getRecentGames(self):
        apiGames = steam.users.get_user_recently_played_games(self.steamID)
        recentGames = {}
        if 'games' in apiGames.keys():
            for game in apiGames['games']:
                name = game['name']
                recentGames[name] = {'appid': game['appid'], 'playtime_forever': float(game['playtime_forever']/60), 'playtime_2weeks': float(game['playtime_2weeks']/60) }
        return recentGames
        


def getAchievementInfo(steamID: str, appid: int):
    achievementDict = {}
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={KEY}&steamid={steamID}&l=en"
    response = requests.get(url)
    # print(apiGameAchievements)
    if response.status_code == 200:
        apiGameAchievements = response.json()
        if 'achievements' in apiGameAchievements['playerstats'].keys():
            for achievement in apiGameAchievements['playerstats']['achievements']:
                apiname = achievement['apiname']
                displayName = achievement['name']
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

def getAcheivementsPerGame(steamID: str, appid: int):
    pass

def describeGame(appid):
    test = steam.apps.get_app_details(appid)
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

def getRarestAchievement(Achievements: dict) -> dict:
    k = ''
    rarest = 101 

    for A in Achievements:
        if Achievements[A]['rarity'] < rarest:
            rarest = Achievements[A]['rarity']
            k = A
    # return rarest
    ans = {}


    if k != '':
        ans[k] = Achievements[k] 
    return ans

if __name__ == '__main__':
    test = {}
    test['apple'] = {}
    test['apple']['rarity'] = 20
    test2 = getRarestAchievement(test)
    print(test2)
    
