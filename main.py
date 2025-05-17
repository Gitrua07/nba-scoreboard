from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv2, boxscoresummaryv2
import datetime

# Get today's date (optional — it defaults to today)
today = datetime.datetime.now().strftime('%Y-%m-%d')

class Game:
#Select a current match
    def __init__(self, game, match):
        self.homeTeam = game[match]['homeTeam']
        self.awayTeam = game[match]['awayTeam']
        self.game = game[match]
        self.gameId = self.game['gameId']

    def getMatchInfo(self):
        print(self.getMatchQuarterTime())
        print(f"{self.awayTeam['teamName']} @ {self.homeTeam['teamName']}")
        #print current score
        print(self.getScore())
        #print score per quarter/team
        print(self.getLineScore())
        #print player stats
        print(self.getPlayerStats())

    #Show current score
    def getScore(self):
        return f'{self.awayTeam['score']} - {self.homeTeam['score']}'

    #Show time left and quarter
    def getMatchQuarterTime(self):
        if(self.game['gameStatusText'] == 'Halftime'):
            return 'HalfTime'

        return f'Q{self.game['period']} - {self.game['gameClock']}'

    def getLineScore(self):
        summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=self.gameId)
        quarterStats = summary.line_score.get_data_frame()
        filterCol = ['TEAM_ABBREVIATION', 'PTS_QTR1', 'PTS_QTR2', 'PTS_QTR3', 'PTS_QTR4', 'PTS']
        return quarterStats[filterCol]

    def getPlayerStats(self):
        box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=self.gameId)
        playerStats = box.player_stats.get_data_frame()
        filterCol = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'MIN', 'REB', 'AST', 'PTS' ]
        return playerStats[filterCol]

#Refresh every 1 - 2 minutes

# Get scoreboard
def getScoreBoard():
        return scoreboard.ScoreBoard()

def main():
    # Each game is represented as a dictionary
    games1 = getScoreBoard().get_dict()['scoreboard']
    games = getScoreBoard().get_dict()['scoreboard']['games']

    # Print basic info
    sum = 0
    for game in games:
        home = game['homeTeam']
        away = game['awayTeam']
    
    print(f"{sum} {away['teamTricode']} ({away['score']}) @ {home['teamTricode']} ({home['score']})")
    sum = sum + 1

    userInput = input("Enter the match number you want to view: ")
    if(int(userInput) > len(games)-1):
        print("Wrong Input - Game does not exist")
        return

    game = Game(games, int(userInput))
    game.getMatchInfo()

if __name__ == '__main__':
    main()
