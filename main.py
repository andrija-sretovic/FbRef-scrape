from bs4 import BeautifulSoup
import requests
import pandas as pd

fbref_url_pl = 'https://fbref.com/en/comps/9/Premier-League-Stats'

response = requests.get(url=fbref_url_pl)
response.raise_for_status()
website = response.text

soup = BeautifulSoup(website, 'html.parser')

table_names = ['stats_squads_standard_for', 'stats_squads_keeper_for', 'stats_squads_keeper_adv_for',
               'stats_squads_shooting_for', 'stats_squads_passing_for', 'stats_squads_passing_types_for',
               'stats_squads_gca_for', 'stats_squads_defense_for', 'stats_squads_possession_for']

team_for_df = pd.DataFrame()

for name in table_names:
    stats_table = soup.find('table', id=name)
    stats = []

    for row in stats_table.find_all('tr'):
        team_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        stats.append(team_data)

    stats_columns = stats[1]
    stats_df = pd.DataFrame(stats[2:], columns=stats_columns)

    print(f'1: {stats_df}')
    if team_for_df.empty:
        team_for_df = stats_df
        print(f'2: {team_for_df}')
    else:
        stats_df.drop(['# Pl', '90s'], axis=1, inplace=True)
        print(f'3: {stats_df}')
        team_for_df = pd.merge(team_for_df, stats_df, on='Squad', suffixes=(name, name))
        print(f'4: {team_for_df}')


print(team_for_df)

