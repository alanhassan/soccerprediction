# imports
import pandas as pd
# imports
import base64
from pickle import TRUE
import requests
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import warnings
from git import Repo
from io import StringIO
import creds

warnings.filterwarnings("ignore")

# serie-A
# trazendo informações mais atualizadas do site https://fbref.com/


print('Start of Campeonato Brasileiro')

all_matches = []
standings_url = "https://fbref.com/en/comps/24/Serie-A-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Série A"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
serie_a_br = match_df

print('End of Campeonato Brasileiro')


print('Start of Serie A')

all_matches = []
standings_url = "https://fbref.com/en/comps/11/Serie-A-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Serie A"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
serie_a = match_df

print('End of Serie A')

# Premier League
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Premier League')

all_matches = []
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Premier League"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
premier_league = match_df

print('End of Premier League')

# La Liga
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of La Liga')

all_matches = []
standings_url = "https://fbref.com/en/comps/12/La-Liga-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "La Liga"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
la_liga = match_df

print('End of La Liga')

# Bundesliga
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Bundesliga')

all_matches = []
standings_url = "https://fbref.com/en/comps/20/Bundesliga-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Bundesliga"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
bundesliga = match_df

print('End of Bundesliga')

# Ligue 1
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Ligue 1')

all_matches = []
standings_url = "https://fbref.com/en/comps/13/Ligue-1-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Ligue 1"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
ligue_1 = match_df

print('End of Ligue 1')

# Primeira Liga - Portugal
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Primeira Liga')

all_matches = []
standings_url = "https://fbref.com/en/comps/32/Primeira-Liga-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Primeira Liga"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
primeira_liga = match_df

print('End of Primeira Liga')

# Eredivisie - Holanda
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Eredivisie')

all_matches = []
standings_url = "https://fbref.com/en/comps/23/Eredivisie-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Eredivisie"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
eredivisie = match_df

print('End of Eredivisie')

# Pro League A - Belgica
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of Pro League A')

all_matches = []
standings_url = "https://fbref.com/en/comps/37/Belgian-Pro-League-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "Pro League A"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
pro_league = match_df

print('End of Pro League A')

# League A - Autralia
# trazendo informações mais atualizadas do site https://fbref.com/

print('Start of League - A')

all_matches = []
standings_url = "https://fbref.com/en/comps/65/A-League-Men-Stats"

data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads' in l]
team_urls = [f"https://fbref.com{l}" for l in links]

for team_url in team_urls:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        
    data = requests.get(team_url)
    matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            
    matches = matches[matches["Comp"] == "A-League"]
    matches["Team"] = team_name
    all_matches.append(matches)
    time.sleep(8)
    
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
league_a = match_df

print('End of League - A')

# consolidando as 6 ligas
match_df = pd.concat([serie_a, premier_league, la_liga, bundesliga, ligue_1, serie_a_br, primeira_liga, eredivisie, pro_league, league_a])

# selecionando apenas as colunas necessárias para o modelo
match_df = match_df[['date', 'comp', 'team', 'opponent', 'venue', 'gf', 'ga', 'result']]

# selecionando até o último jogo disponível
match_df = match_df[~pd.isna(match_df['gf'])]

# inserindo a base de histórico (antes de '2023-08-01'), para conseguir pegar os resultados dos últimos confrontos entre os times
# url_leagues = 'https://github.com/alanhassan/soccerprediction/blob/main/leagues.xlsx?raw=true'
# data = requests.get(url_leagues).content
# leagues = pd.read_excel(data)

url_leagues = 'https://github.com/alanhassan/soccerprediction/blob/main/leagues.xlsx?raw=true'
data_leagues = requests.get(url_leagues).content
leagues = pd.read_excel(data_leagues)

leagues = leagues[['date', 'comp', 'team', 'opponent', 'venue', 'gf', 'ga', 'result']]
leagues['date'] = pd.to_datetime(leagues['date'])
leagues = leagues[leagues['date'] < pd.to_datetime('2023-08-01')]


# adicionando a base 'leagues' com a 'match_df'
match_df_final_all = pd.concat([leagues, match_df])

# inserindo uma coluna com a pontuação obtida em cada partida
match_df_final_all['pont'] = match_df_final_all['result'].replace({'L': 0, 'D': 1, 'W':3})

# ajustando data
match_df_final_all['date'] = pd.to_datetime(match_df_final_all['date'])

# ajustando nomes dos times
match_df_final_all = match_df_final_all.replace({'opponent' : { 'Inter' : 'Internazionale',
                                        'Manchester Utd' : 'Manchester United',
                                        'Tottenham' : 'Tottenham Hotspur',
                                        'West Ham' : 'West Ham United',
                                        'Newcastle Utd' : 'Newcastle United',
                                        "Nott'ham Forest" : 'Nottingham Forest',
                                        'Wolves' : 'Wolverhampton Wanderers',
                                        'Brighton' : 'Brighton and Hove Albion',
                                        'Almería' : 'Almeria',
                                        'Betis' : 'Real Betis',
                                        'Atlético Madrid' : 'Atletico Madrid',
                                        'Alavés': 'Alaves',
                                        'Cádiz' : 'Cadiz',
                                        'Köln' : 'Koln',
                                        'Eint Frankfurt' : 'Eintracht Frankfurt',
                                        "M'Gladbach" : 'Monchengladbach',
                                        'Leverkusen' : 'Bayer Leverkusen',
                                        'Paris S-G' : 'Paris Saint Germain',
                                        'Vitória' : 'Vitoria',
                                        'Atl Goianiense' : 'Atletico Goianiense',
                                        'São Paulo' : 'Sao Paulo',
                                        'Grêmio' : 'Gremio',
                                        'Botafogo (RJ)' : 'Botafogo RJ',
                                        'Ath Paranaense' : 'Athletico Paranaense',
                                        'Avaí' : 'Avai',
                                        'Atlético Mineiro' : 'Atletico Mineiro',
                                        'Ceará' : 'Ceara',
                                        'Paraná' : 'Parana',
                                        'América (MG)' : 'America MG',
                                        'Goiás' : 'Goias',
                                        'Cuiabá' : 'Cuiaba',
                                        'Famalicão': 'Famalicao',
                                        'Vitória': 'Vitoria Guimaraes',
                                        'Go Ahead Eag': 'Go Ahead Eagles',
                                        "Sparta R'dam": 'Sparta Rotterdam',
                                        'Sint-Truiden': 'Sint Truiden',
                                        'Standard Liège': 'Standard Liege',
                                        'Adelaide': 'Adelaide United',
                                        'Brisbane': 'Brisbane Roar',
                                        'Central Coast': 'Central Coast Mariners',
                                        'Melb City': 'Melbourne City',
                                        'Melb Victory': 'Melbourne Victory',
                                        'Newcastle': 'Newcastle Jets',
                                        'W Sydney': 'Western Sydney Wanderers',
                                        'Wellington': 'Wellington Phoenix'}})

# último resultado do confronto entre os times
# sort the DataFrame by date
match_df_final_all = match_df_final_all.sort_values(by='date').reset_index(drop=True)

# group the DataFrame by the home team and away team
grouped = match_df_final_all.groupby(['team', 'opponent'])

# create a new column that contains the sum of the last two results for each group
grouped_result = grouped['pont'].apply(lambda x: x.rolling(2, closed='right').sum())

grouped_result = grouped_result.droplevel(['team', 'opponent']).sort_index()

match_df_final_all['last_2_results_sum'] = grouped_result.values

# filtrando a data, para considerar apenas os jogos da temporada atual (temporada começa em agosto)
match_df_final = match_df_final_all[match_df_final_all['date'] >= pd.to_datetime('2022-08-01')]

# alterando o parâmetro do closed para "right", pois agora queremos incluir o resultado do jogo mais recente na previsão
def rolling_sum(group, cols, new_cols, venue):
    group = group[group['venue'] == venue]
    group = group.sort_values('date')
    
    if len(group) >= 3:
        rolling_stats = group[cols].rolling(3, closed='right').sum()
        group[new_cols] = rolling_stats
    elif len(group) == 2:
        rolling_stats = group[cols].rolling(2, closed='right').sum()
        group[new_cols] = rolling_stats
    elif len(group) == 1:
        rolling_stats = group[cols].rolling(1, closed='right').sum()
        group[new_cols] = rolling_stats
    else:
        group[new_cols] = None
        
    group = group.dropna(subset=new_cols)
    return group

# Filter rows that don't contain '(' in the specified column
match_df_final = match_df_final[~match_df_final['gf'].str.contains('\(', na=False)]

# Reset the index if needed
match_df_final.reset_index(drop=True, inplace=True)

# inserindo colunas rolling
df_rolling_home = match_df_final.groupby('team').apply(lambda x: rolling_sum(x, ['gf', 'ga', 'pont'], ['gf_rolling', 'ga_rolling', 'pont_rolling'], 'Home'))
df_rolling_home = df_rolling_home.droplevel('team')

df_rolling_away = match_df_final.groupby('team').apply(lambda x: rolling_sum(x, ['gf', 'ga', 'pont'], ['gf_rolling', 'ga_rolling', 'pont_rolling'], 'Away'))
df_rolling_away = df_rolling_away.droplevel('team')

# incluindo variáveis rolling do time jogando fora de casa
df_rolling = df_rolling_home.merge(df_rolling_away, left_on=['date', 'opponent'], right_on=['date', 'team'], suffixes=('_home','_away'), how='inner')

# inserindo as informações de "Points last season"

url_additional = 'https://github.com/alanhassan/soccerprediction/blob/main/additional.xlsx?raw=true'
data_additional = requests.get(url_additional).content
additional = pd.read_excel(data_additional)

df_rolling = df_rolling.merge(additional, how = 'left', left_on='team_home', right_on='team')
df_rolling.rename(columns={"Points last season_": "Points last season_home"}, inplace=True)

df_rolling = df_rolling.merge(additional, how = 'left', left_on='opponent_home', right_on='team')
df_rolling.rename(columns={"Points last season_": "Points last season_away",
                        "team_home": "home",
                        "team_away": "away",
                        "comp_home": "comp"}, inplace=True)

# valores para os times que subiram de divisão (média dos times que subiram de divisão)
values = {"Points last season_home": 35, "Points last season_away": 35}
df_rolling.fillna(value=values, inplace=True)

# filtrando apenas colunas que serão necessárias para o modelo
df_rolling = df_rolling[['date', 'comp', 'home', 'gf_rolling_home',
            'ga_rolling_home', 'pont_rolling_home', 'Points last season_home', 'last_2_results_sum_home',
            'away', 'gf_rolling_away', 'ga_rolling_away',
            'pont_rolling_away', 'Points last season_away']]

# renomeando coluna "last_2_results_sum_home"
df_rolling.rename(columns={"last_2_results_sum_home": "last_2_results"}, inplace=True)


# Function to push DataFrame to GitHub
def push_dataframe_to_github(dataframe, file_name, repository):
    # Convert DataFrame to CSV in-memory
    csv_data = StringIO()
    dataframe.to_csv(csv_data, index=False)
    csv_content = csv_data.getvalue()

    # Encode content to Base64
    encoded_content = base64.b64encode(csv_content.encode()).decode()

    # Check if the file exists
    url_get = f'https://api.github.com/repos/{username}/{repository}/contents/{file_name}'
    headers_get = {'Authorization': f'token {creds.token}'}

    response_get = requests.get(url_get, headers=headers_get)
    response_get_json = response_get.json()

    # Extract the SHA from the response
    current_sha = response_get_json.get('sha')

    # Push data directly to GitHub using GitHub API
    url_put = f'https://api.github.com/repos/{username}/{repository}/contents/{file_name}'
    headers_put = {
        'Authorization': f'token {creds.token}',
        'Content-Type': 'application/json'
    }

    data_put = {
        'message': f'Update {file_name}',
        'content': encoded_content
    }

    # If the file exists, update it; otherwise, create it
    if current_sha is not None:
        data_put['sha'] = current_sha

    response_put = requests.put(url_put, headers=headers_put, json=data_put)

    if response_put.status_code == 200:
        print(f'Data pushed to {file_name} on GitHub successfully!')
    elif response_put.status_code == 201:
        print(f'{file_name} created on GitHub successfully!')
    else:
        print(f'Error: {response_put.status_code}, {response_put.text}')

# GitHub repository details
username = 'alanhassan'
repository = 'soccerprediction'

# Push each DataFrame to GitHub
push_dataframe_to_github(df_rolling, 'df_rolling.csv', repository)
push_dataframe_to_github(match_df_final_all, 'match_df_final_all.csv', repository)

