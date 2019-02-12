# Date: February 11th 2019
# Authors: D.B., H.W. 
#

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay


for item in teams.get_teams():
	print(item['nickname'], item['abbreviation'])


def get_stats(team_abbr):

	'''
	This function will return the last game stats of a particlar team.

	Parameters:
	team_abbr: pass a string with the abbreviation of a particular team

	example> get_stats('CHI')
	'''

	nba_teams = teams.get_teams()


	# Select the dictionary for the Pacers, which contains their team ID
	nba_team = [team for team in nba_teams if team['abbreviation'] == team_abbr][0]
	nba_team_id = nba_team['id']

	# Query for the last regular season game where the Pacers were playing

	gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=nba_team_id,
	                            season_nullable=Season.default,
	                            season_type_nullable=SeasonType.regular)  

	games_dict = gamefinder.get_normalized_dict()
	games = games_dict['LeagueGameFinderResults']
	game = games[0]
	game_id = game['GAME_ID']
	game_matchup = game['MATCHUP']

	print(f'Searching through {len(games)} game(s) for the game_id of {game_id} where {game_matchup}')

	# Query for the play by play of that most recent regular season game
	df = playbyplay.PlayByPlay(game_id).get_data_frames()[0]
	df.head() #just looking at the head of the data

	df.to_csv(team_abbr+'_'+str(game_id)+'.csv')

	return print('stats have been exported in the working folder!')


def get_stats_all():
	'''
	This function will return last game stats for each NBA team. 
	'''
	for team in teams.get_teams():
		try:
			get_stats(team['abbreviation'])
			print('processing...')
		except:
			print('Timed out for requests...need to wait for a while and retry.')
	print('done!')




