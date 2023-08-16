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
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import base64
import joblib
from io import BytesIO
from github import Github

warnings.filterwarnings("ignore")

# conectando com github

#token

key = os.environ.get('API_Key')
g = Github(key)

#repositório
repo = g.get_repo("alanhassan/soccerprediction")

# df_rolling
url_df = 'https://github.com/alanhassan/soccerprediction/blob/main/df_rolling.xlsx?raw=true'
data = requests.get(url_df).content
df_rolling = pd.read_excel(data)

# match_df_final
url_df_l2r = 'https://github.com/alanhassan/soccerprediction/blob/main/match_df_final_all.xlsx?raw=true'
data_l2r = requests.get(url_df_l2r).content
match_df_final_all = pd.read_excel(data_l2r)

#get ml model from github
url_ml = 'https://github.com/alanhassan/soccerprediction/blob/main/best_lr.pkl?raw=true'

file = BytesIO(requests.get(url_ml).content)

ml = joblib.load(file)

ml.fitted_ = True

# funções 
# func home
def home(df, team):
    df = df.sort_values(by=['date'])
    df = df[df['home'] == f'{team}'][-1:].drop(columns = ['date', 'comp', 'home', 'away',
                                                            'gf_rolling_away', 'ga_rolling_away',
                                                            'pont_rolling_away', 'Points last season_away'
                                                            ], inplace=False)
    df.rename(columns={"gf_rolling_home": "gf_rolling",
                            "ga_rolling_home": "ga_rolling",
                            "pont_rolling_home": "pont_rolling",
                            "Points last season_home": "Points last season"}, inplace=True)
    df = df[['Points last season', 'pont_rolling', 'gf_rolling', 'ga_rolling']].reset_index(drop=True)
    return df

# func away
def away(df, team):
    df = df.sort_values(by=['date'])
    df = df[df['away'] == f'{team}'][-1:].drop(columns = ['date', 'comp', 'home', 'away',
                                                            'gf_rolling_home', 'ga_rolling_home',
                                                            'pont_rolling_home', 'Points last season_home'
                                                            ], inplace=False)
    df.rename(columns={"gf_rolling_away": "gf_rolling",
                            "ga_rolling_away": "ga_rolling",
                            "pont_rolling_away": "pont_rolling",
                            "Points last season_away": "Points last season"}, inplace=True)
    df = df[['Points last season', 'pont_rolling', 'gf_rolling', 'ga_rolling']].reset_index(drop=True)
    df['pont_rolling'].replace(0, 1, inplace=True)
    df['gf_rolling'].replace(0, 1, inplace=True)
    df['ga_rolling'].replace(0, 1, inplace=True)
    return df

# func ratio
def ratio(df, team1, team2):
    df = home(df, f'{team1}')/away(df, f'{team2}')
    df.rename(columns={"Points last season": "points_last_season_ratio",
                        "pont_rolling": "pont_rolling_ratio",
                        "gf_rolling": "gf_rolling_ratio",
                        "ga_rolling": "ga_rolling_ratio"}, inplace=True)
    return df

# func for 'last_2_results'
def last_2_results(df, team1, team2):
    df = match_df_final_all.sort_values(by='date').reset_index(drop=True)
    length = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].shape[0]
    if length >= 2:
        last_2_results_sum = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].iloc[-1]['last_2_results_sum']
    elif length == 1:
        last_2_results_sum = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].iloc[-1]['pont']
    elif length == 0:
        last_2_results_sum = 1
    return last_2_results_sum


# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome('chromedriver',options=options)

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get("https://www.flashscore.com/")

# Fechando Botão de Cookies
try:
    button_cookies = wd_Chrome.find_element(By.CSS_SELECTOR,'button#onetrust-accept-btn-handler')
    button_cookies.click()
except:
    pass

ids = []  # create an empty list to store IDs

time.sleep(5)
for i in range(6):

    # Selecionando o dia de amanhã
    wd_Chrome.find_element(By.CSS_SELECTOR,'button.calendar__navigation--tomorrow').click()
    time.sleep(3)

    # Pegando o ID dos Jogos
    id_jogos = []
    jogos = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.event__match--scheduled')

    for i in jogos:
        id_jogos.append(i.get_attribute("id"))

    # Exemplo de ID de um jogo: 'g_1_Gb7buXVt'    
    id_jogos = [i[4:] for i in id_jogos]
    
    ids.append(id_jogos)
        
    i=+1

jogo = {'Date':[],'Time':[],'Country':[],'League':[],'Home':[],'Away':[],'Odds_H':[],'Odds_D':[],'Odds_A':[]}    

final_ids = []
for sublist in ids:
    final_ids.extend(sublist)


# Pegando as Informacoes Básicas do Jogo
for link in tqdm(final_ids, total=len(final_ids)):
    wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/match-summary')
    
    try:
        Date = wd_Chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__startTime').text.split(' ')[0]
        Time = wd_Chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__startTime').text.split(' ')[1]
        Country = wd_Chrome.find_element(By.CSS_SELECTOR,'span.tournamentHeader__country').text.split(':')[0]
        League = wd_Chrome.find_element(By.CSS_SELECTOR,'span.tournamentHeader__country')
        League = League.find_element(By.CSS_SELECTOR,'a').text
        Home = wd_Chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__home')
        Home = Home.find_element(By.CSS_SELECTOR,'div.participant__participantName').text
        Away = wd_Chrome.find_element(By.CSS_SELECTOR,'div.duelParticipant__away')
        Away = Away.find_element(By.CSS_SELECTOR,'div.participant__participantName').text
    except:
        pass

# Match Odds
    try:
        wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/odds-comparison/1x2-odds/full-time')
        time.sleep(2)
        
        linhas = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.ui-table__row')
        
        for linha in linhas:
                Odds_H = linha.find_elements(By.CSS_SELECTOR,'a.oddsCell__odd')[0].text
                Odds_D = linha.find_elements(By.CSS_SELECTOR,'a.oddsCell__odd')[1].text 
                Odds_A = linha.find_elements(By.CSS_SELECTOR,'a.oddsCell__odd')[2].text
    except:
        pass

    print(Date,Time,Country,League,Home,Away,Odds_H,Odds_D,Odds_A) 
    
    jogo['Date'].append(Date)
    jogo['Time'].append(Time)
    jogo['Country'].append(Country)
    jogo['League'].append(League)
    jogo['Home'].append(Home)
    jogo['Away'].append(Away)
    jogo['Odds_H'].append(Odds_H)
    jogo['Odds_D'].append(Odds_D)
    jogo['Odds_A'].append(Odds_A)

df = pd.DataFrame(jogo)
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)

# filtrando o df

df_filtered = df[(df['Country'].str.contains('ENGLAND|GERMANY|SPAIN|ITALY|FRANCE|BRAZIL'))]
df_filtered = df_filtered[(df_filtered['League'].str.contains('PREMIER LEAGUE|BUNDESLIGA|LALIGA|LIGUE 1|SERIE A'))]
df_filtered = df_filtered[~(df_filtered['League'].str.contains('LALIGA2|2. BUNDESLIGA|WOMEN|JUNIOREN|PLAY OFFS|RELEGATION'))]
df_filtered['Date'] = pd.to_datetime(df_filtered['Date'].str.replace('.', '/'), format='%d/%m/%Y').dt.date
df_filtered = df_filtered.sort_values(by=['Date', 'Country'])

# renomeando
df_odds = df_filtered

# ajustando nomes dos times para ficar igual ao das outras bases
df_odds = df_odds.replace({'Home' : { 'Leeds' : 'Leeds United',
                                        'Leicester' : 'Leicester City',
                                        'Wolves' : 'Wolverhampton Wanderers',
                                        'Hertha Berlin' : 'Hertha BSC',
                                        'Mainz' : 'Mainz 05',
                                        'Verona' : 'Hellas Verona',
                                        'Manchester Utd' : 'Manchester United',
                                        'AC Ajaccio' : 'Ajaccio',
                                        'B. Monchengladbach' : 'Monchengladbach',
                                        'AC Milan' : 'Milan',
                                        'Betis' : 'Real Betis',
                                        'Tottenham' : 'Tottenham Hotspur',
                                        'Brighton' : 'Brighton and Hove Albion',
                                        'Nottingham' : 'Nottingham Forest',                                 
                                        'Schalke' : 'Schalke 04',
                                        'Inter' : 'Internazionale',
                                        'Ath Bilbao' : 'Athletic Club',
                                        'Cadiz CF' : 'Cadiz',
                                        'West Ham' : 'West Ham United',
                                        'Newcastle' : 'Newcastle United',
                                        'Clermont' : 'Clermont Foot',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Atletico Paranaense',
                                        'Vasco' : 'Vasco da Gama'
                                        }})

df_odds = df_odds.replace({'Away' : { 'Leeds' : 'Leeds United',
                                        'Leicester' : 'Leicester City',
                                        'Wolves' : 'Wolverhampton Wanderers',
                                        'Hertha Berlin' : 'Hertha BSC',
                                        'Mainz' : 'Mainz 05',
                                        'Verona' : 'Hellas Verona',
                                        'Manchester Utd' : 'Manchester United',
                                        'AC Ajaccio' : 'Ajaccio',
                                        'B. Monchengladbach' : 'Monchengladbach',
                                        'AC Milan' : 'Milan',
                                        'Betis' : 'Real Betis',
                                        'Tottenham' : 'Tottenham Hotspur',
                                        'Brighton' : 'Brighton and Hove Albion',
                                        'Nottingham' : 'Nottingham Forest',                                 
                                        'Schalke' : 'Schalke 04',
                                        'Inter' : 'Internazionale',
                                        'Ath Bilbao' : 'Athletic Club',
                                        'Cadiz CF' : 'Cadiz',
                                        'West Ham' : 'West Ham United',
                                        'Newcastle' : 'Newcastle United',
                                        'Clermont' : 'Clermont Foot',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Atletico Paranaense',
                                        'Vasco' : 'Vasco da Gama'}})

df_odds = df_odds.reset_index()
# previsões de ml
prediction_home = []
for i in range(0,len(df_odds)):
    pred = ratio(df_rolling, df_odds['Home'][i], df_odds['Away'][i])
    pred['last_2_results'] = last_2_results(df_rolling, df_odds['Home'][i], df_odds['Away'][i])
    
    # Handle missing values in 'pred' DataFrame, if any
    pred.fillna(0, inplace=True)

prediction = ml.predict_proba(pred)[0][1]
prediction_home.append(prediction)

# adicionando coluna
df_odds['Pred_H'] = prediction_home
df_odds['Pred_A'] = 1 - df_odds['Pred_H']

# formatando
df_odds['Pred_H'] = df_odds['Pred_H'].round(2)
df_odds['Pred_A'] = df_odds['Pred_A'].round(2)


# Gerando os dados para excel
df_odds.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/df_odds.xlsx')

# update no Github
repo = Repo('C:/Users/alan.hassan/Desktop/github/soccerprediction')  # if repo is CWD just do '.'
origin = repo.remote('origin')
assert origin.exists()
origin.fetch()
repo.git.pull('origin','main')
repo.index.add('df_odds.xlsx')
repo.index.commit("your commit message")
repo.git.push("--set-upstream", origin, repo.head.ref)

