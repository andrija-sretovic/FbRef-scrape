from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

today = datetime.today().strftime('%d-%m-%Y')

fbref_url_pl = 'https://fbref.com/en/comps/9/Premier-League-Stats'

response = requests.get(url=fbref_url_pl)
response.raise_for_status()
website = response.text

soup = BeautifulSoup(website, 'html.parser')

table_names = ['stats_squads_standard_for', 'stats_squads_keeper_for', 'stats_squads_keeper_adv_for',
               'stats_squads_shooting_for', 'stats_squads_passing_for', 'stats_squads_passing_types_for',
               'stats_squads_gca_for', 'stats_squads_defense_for', 'stats_squads_possession_for']

table_names_agg = ['stats_squads_standard_against', 'stats_squads_keeper_against', 'stats_squads_keeper_adv_against',
                   'stats_squads_shooting_against', 'stats_squads_passing_against', 'stats_squads_passing_types_against',
                   'stats_squads_gca_against', 'stats_squads_defense_against', 'stats_squads_possession_against']


team_for_df = pd.DataFrame()
team_agg_df = pd.DataFrame()

# Get data for teams when attacking

for name in table_names:
    stats_table = soup.find('table', id=name)
    stats = []

    for row in stats_table.find_all('tr'):
        team_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        stats.append(team_data)

    stats_columns = stats[1]
    stats_df = pd.DataFrame(stats[2:], columns=stats_columns)

    if team_for_df.empty:
        team_for_df = stats_df
    else:
        stats_df.drop(['# Pl', '90s'], axis=1, inplace=True)
        team_for_df = pd.merge(team_for_df, stats_df, on='Squad', how='left',
                               suffixes=(f'-{name.split("_")[-2]}', f'-{name.split("_")[-2]}'))

team_for_df.to_csv(f'PL team stats-{today}.csv', index=False)

# Get data for teams when defending

for name in table_names_agg:
    stats_table = soup.find('table', id=name)
    stats_agg = []

    for row in stats_table.find_all('tr'):
        team_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        stats_agg.append(team_data)

    stats_agg_columns = stats_agg[1]
    stats_agg_df = pd.DataFrame(stats_agg[2:], columns=stats_agg_columns)

    if team_agg_df.empty:
        team_agg_df = stats_agg_df
    else:
        stats_agg_df.drop(['# Pl', '90s'], axis=1, inplace=True)
        team_agg_df = pd.merge(team_agg_df, stats_agg_df, on='Squad', how='left',
                               suffixes=(f'-{name.split("_")[-2]}', f'-{name.split("_")[-2]}'))

team_agg_df.to_csv(f'PL team stats agg-{today}.csv', index=False)

