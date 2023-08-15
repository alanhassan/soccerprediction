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


# consolidando as 6 ligas
match_df = pd.concat([serie_a, premier_league, la_liga, bundesliga, ligue_1, serie_a_br])

# selecionando apenas as colunas necessárias para o modelo
match_df = match_df[['date', 'comp', 'team', 'opponent', 'venue', 'gf', 'ga', 'result']]

# selecionando até o último jogo disponível
match_df = match_df[~pd.isna(match_df['gf'])]

# inserindo a base de histórico (antes de '2023-08-01'), para conseguir pegar os resultados dos últimos confrontos entre os times
url_leagues = 'https://github.com/alanhassan/soccerprediction/blob/main/leagues.xlsx?raw=true'
data = requests.get(url_leagues).content
leagues = pd.read_excel(data)
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
                                        'Atl Paranaense' : 'Atletico Paranaense',
                                        'Avaí' : 'Avai',
                                        'Atlético Mineiro' : 'Atletico Mineiro',
                                        'Ceará' : 'Ceara',
                                        'Paraná' : 'Parana',
                                        'América (MG)' : 'America MG',
                                        'Goiás' : 'Goias',
                                        'Cuiabá' : 'Cuiaba'}})


# último resultado do confronto entre os times
# sort the DataFrame by date
match_df_final_all = match_df_final_all.sort_values(by='date').reset_index(drop=True)

# group the DataFrame by the home team and away team
grouped = match_df_final_all.groupby(['team', 'opponent'])

# create a new column that contains the sum of the last two results for each group
match_df_final_all['last_2_results_sum'] = grouped['pont'].apply(lambda x: x.rolling(2, closed='right').sum())


# filtrando a data, para considerar apenas os jogos da temporada atual (temporada começa em agosto)
match_df_final = match_df_final_all[match_df_final_all['date'] >= pd.to_datetime('2022-08-01')]

# alterando o parâmetro do closed para "right", pois agora queremos incluir o resultado do jogo mais recente na previsão
def rolling_sum(group, cols, new_cols, venue):
    group = group[group['venue'] == venue]
    group = group.sort_values('date')
    rolling_stats = group[cols].rolling(3, closed='right').sum()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

# inserindo colunas rolling
df_rolling_home = match_df_final.groupby('team').apply(lambda x: rolling_sum(x, ['gf', 'ga', 'pont'], ['gf_rolling', 'ga_rolling', 'pont_rolling'], 'Home'))
df_rolling_home = df_rolling_home.droplevel('team')

df_rolling_away = match_df_final.groupby('team').apply(lambda x: rolling_sum(x, ['gf', 'ga', 'pont'], ['gf_rolling', 'ga_rolling', 'pont_rolling'], 'Away'))
df_rolling_away = df_rolling_away.droplevel('team')

# incluindo variáveis rolling do time jogando fora de casa
df_rolling = df_rolling_home.merge(df_rolling_away, left_on=['date', 'opponent'], right_on=['date', 'team'], suffixes=('_home','_away'), how='inner')


# inserindo as informações de "Points last season"
#url_add = 'https://github.com/alanhassan/soccerprediction/blob/main/additional.xlsx?raw=true'
additional = pd.read_excel(r'C:\Users\alan.hassan\Desktop\github\soccerprediction\additional.xlsx')

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


df_rolling.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/df_rolling.xlsx')
match_df_final_all.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/match_df_final_all.xlsx')

# update no Github

repo = Repo('C:/Users/alan.hassan/Desktop/github/soccerprediction')  # if repo is CWD just do '.'
origin = repo.remote('origin')
assert origin.exists()
origin.fetch()
repo.git.pull('origin','main')
repo.index.add('df_rolling.xlsx')
repo.index.add('match_df_final_all.xlsx')
repo.index.commit("your commit message")
repo.git.push("--set-upstream", origin, repo.head.ref)

