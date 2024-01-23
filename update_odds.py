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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import base64
import joblib
from io import BytesIO
from github import Github
from io import StringIO
import creds

warnings.filterwarnings("ignore")

# conectando com github

#token

# key = os.environ.get('API_Key')
# g = Github(key)

# #repositório
# repo = g.get_repo("alanhassan/soccerprediction")

# df_rolling
url_df = 'https://github.com/alanhassan/soccerprediction/blob/main/df_rolling.csv?raw=true'
data = requests.get(url_df).content
df_rolling = pd.read_csv(BytesIO(data))

# match_df_final
url_df_l2r = 'https://github.com/alanhassan/soccerprediction/blob/main/match_df_final_all.csv?raw=true'
data_l2r = requests.get(url_df_l2r).content
match_df_final_all = pd.read_csv(BytesIO(data_l2r))

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



service=Service(ChromeDriverManager().install())

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# GitHub repository details
username = 'alanhassan'
repository = 'soccerprediction'


# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=service, options=options)

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
for i in range(5):

    # jogos de hoje

    # Pegando o ID dos Jogos
    id_jogos = []
    jogos = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.event__match--scheduled')

    for i in jogos:
        id_jogos.append(i.get_attribute("id"))

    # Exemplo de ID de um jogo: 'g_1_Gb7buXVt'    
    id_jogos = [i[4:] for i in id_jogos]
    
    ids.append(id_jogos)

    # Selecionando o dia de amanhã
    wd_Chrome.find_element(By.CSS_SELECTOR,'button.calendar__navigation--tomorrow').click()
    time.sleep(3)
        
    i=+1

jogo = {'Date':[],'Time':[],'Country':[],'League':[],'Home':[],'Away':[],'Odds_H':[],'Odds_D':[],'Odds_A':[]}    

final_ids = []
for sublist in ids:
    final_ids.extend(sublist)


# Pegando as Informacoes Básicas do Jogo
for link in tqdm(final_ids, total=len(final_ids)):
    wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/match-summary')
    
    try:
        Date = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[0]
        Time = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[1]
        Country = wd_Chrome.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country').text.split(':')[0]
        League = wd_Chrome.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country')
        League = League.find_element(By.CSS_SELECTOR, 'a').text
        Home = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__home')
        Home = Home.find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        Away = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__away')
        Away = Away.find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
    except:
        continue  # Skip to the next iteration if basic information retrieval fails

    # Match Odds
    try:
        wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/odds-comparison/1x2-odds/full-time')
        time.sleep(2)

        # Check if redirected to match summary page
        if 'match-summary' in wd_Chrome.current_url:
            continue  # Skip to the next iteration if redirected to match summary page

        linhas = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.ui-table__row')

        for linha in linhas:
            Odds_H = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text
            Odds_D = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text
            Odds_A = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[2].text
    except:
        continue  # Skip to the next iteration if odds information retrieval fails

    #print(Date, Time, Country, League, Home, Away, Odds_H, Odds_D, Odds_A)
    
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

df_filtered = df[(df['Country'].str.contains('ENGLAND|GERMANY|SPAIN|ITALY|FRANCE|BRAZIL|PORTUGAL|NETHERLANDS|BELGIUM|AUSTRALIA'))]
df_filtered = df_filtered[(df_filtered['League'].str.contains('PREMIER LEAGUE|BUNDESLIGA|LALIGA|LIGUE 1|SERIE A|LIGA PORTUGAL|EREDIVISIE|JUPILER PRO LEAGUE|A-LEAGUE'))]
df_filtered = df_filtered[~(df_filtered['League'].str.contains('LALIGA2|2. BUNDESLIGA|WOMEN|JUNIOREN|PLAY OFFS|RELEGATION|CUP|LIGA PORTUGAL 2'))]
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
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Luton' : 'Luton Town',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Athletico Paranaense',
                                        'Vasco' : 'Vasco da Gama',
                                        'SC Farense': 'Farense',
                                        'Gil Vicente': 'Gil Vicente FC',
                                        'FC Porto': 'Porto',
                                        'FC Volendam': 'Volendam',
                                        'G.A. Eagles': 'Go Ahead Eagles',
                                        'Heracles': 'Heracles Almelo',
                                        'Nijmegen': 'NEC Nijmegen',
                                        'PSV': 'PSV Eindhoven',
                                        'Sittard': 'Fortuna Sittard',
                                        'Waalwijk': 'RKC Waalwijk',
                                        'Cercle Brugge KSV': 'Cercle Brugge',
                                        'Club Brugge KV': 'Club Brugge',
                                        'KV Mechelen': 'Mechelen',
                                        'Leuven': 'OH Leuven',
                                        'Royale Union SG': 'Union SG',
                                        'RWDM': 'RWD Molenbeek',
                                        'St. Liege': 'Standard Liege',
                                        'St. Truiden': 'Sint Truiden',
                                        'WS Wanderers': 'Western Sydney Wanderers'
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
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Luton' : 'Luton Town',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Atletico Paranaense',
                                        'Vasco' : 'Vasco da Gama',
                                        'SC Farense': 'Farense',
                                        'Gil Vicente': 'Gil Vicente FC',
                                        'FC Porto': 'Porto',
                                        'FC Volendam': 'Volendam',
                                        'G.A. Eagles': 'Go Ahead Eagles',
                                        'Heracles': 'Heracles Almelo',
                                        'Nijmegen': 'NEC Nijmegen',
                                        'PSV': 'PSV Eindhoven',
                                        'Sittard': 'Fortuna Sittard',
                                        'Waalwijk': 'RKC Waalwijk',
                                        'Cercle Brugge KSV': 'Cercle Brugge',
                                        'Club Brugge KV': 'Club Brugge',
                                        'KV Mechelen': 'Mechelen',
                                        'Leuven': 'OH Leuven',
                                        'Royale Union SG': 'Union SG',
                                        'RWDM': 'RWD Molenbeek',
                                        'St. Liege': 'Standard Liege',
                                        'St. Truiden': 'Sint Truiden',
                                        'WS Wanderers': 'Western Sydney Wanderers'
                                        }})

df_odds = df_odds.reset_index()
# previsões de ml
prediction_home = []
for i in range(0, len(df_odds)):
    pred = ratio(df_rolling, df_odds['Home'][i], df_odds['Away'][i])
    pred['last_2_results'] = last_2_results(df_rolling, df_odds['Home'][i], df_odds['Away'][i])
    
    # Check if there are any NaN values in 'pred' DataFrame
    if pred.isnull().values.any():
        prediction = None  # Skip prediction for this row
    else:
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


# Push each DataFrame to GitHub
push_dataframe_to_github(df_odds, 'df_odds.csv', repository)

# get data

url_df_odds = 'https://github.com/alanhassan/soccerprediction/blob/main/df_odds.csv?raw=true'
data_odds = requests.get(url_df_odds).content
df_odds = pd.read_csv(BytesIO(data_odds))


# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=service, options=options)


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
for i in range(5):

    # Pegando o ID dos Jogos
    id_jogos = []
    jogos = wd_Chrome.find_elements(By.CSS_SELECTOR,'div.event__match--scheduled')

    for i in jogos:
        id_jogos.append(i.get_attribute("id"))

    # Exemplo de ID de um jogo: 'g_1_Gb7buXVt'    
    id_jogos = [i[4:] for i in id_jogos]
    
    ids.append(id_jogos)

    # Selecionando o dia de amanhã
    wd_Chrome.find_element(By.CSS_SELECTOR,'button.calendar__navigation--tomorrow').click()
    time.sleep(3)
        
    i=+1

jogo = {'Date':[],'Time':[],'Country':[],'League':[],'Home':[],'Away':[],'Odds_H_X':[],'Odds_H_A':[],'Odds_X_A':[]}    

final_ids = []
for sublist in ids:
    final_ids.extend(sublist)


# Pegando as Informacoes Básicas do Jogo
for link in tqdm(final_ids, total=len(final_ids)):
    wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/match-summary')
    
    try:
        Date = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[0]
        Time = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__startTime').text.split(' ')[1]
        Country = wd_Chrome.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country').text.split(':')[0]
        League = wd_Chrome.find_element(By.CSS_SELECTOR, 'span.tournamentHeader__country')
        League = League.find_element(By.CSS_SELECTOR, 'a').text
        Home = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__home')
        Home = Home.find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
        Away = wd_Chrome.find_element(By.CSS_SELECTOR, 'div.duelParticipant__away')
        Away = Away.find_element(By.CSS_SELECTOR, 'div.participant__participantName').text
    except:
        continue  # Skip to the next iteration if basic information retrieval fails

    # Match Odds
    try:
        wd_Chrome.get(f'https://www.flashscore.com/match/{link}/#/odds-comparison/double-chance/full-time')
        time.sleep(2)

        # Check if redirected to match summary page
        if 'match-summary' in wd_Chrome.current_url:
            continue  # Skip to the next iteration if redirected to match summary page

        linhas = wd_Chrome.find_elements(By.CSS_SELECTOR, 'div.ui-table__row')

        for linha in linhas:
            Odds_H_X = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[0].text
            Odds_H_A = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[1].text
            Odds_X_A = linha.find_elements(By.CSS_SELECTOR, 'a.oddsCell__odd')[2].text
    except:
        continue  # Skip to the next iteration if odds information retrieval fails

    
    jogo['Date'].append(Date)
    jogo['Time'].append(Time)
    jogo['Country'].append(Country)
    jogo['League'].append(League)
    jogo['Home'].append(Home)
    jogo['Away'].append(Away)
    jogo['Odds_H_X'].append(Odds_H_X)
    jogo['Odds_H_A'].append(Odds_H_A)
    jogo['Odds_X_A'].append(Odds_X_A)
    time.sleep(2)

df = pd.DataFrame(jogo)
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)

# filtrando o df

df_filtered = df[(df['Country'].str.contains('ENGLAND|GERMANY|SPAIN|ITALY|FRANCE|BRAZIL|PORTUGAL|NETHERLANDS|BELGIUM|AUSTRALIA'))]
df_filtered = df_filtered[(df_filtered['League'].str.contains('PREMIER LEAGUE|BUNDESLIGA|LALIGA|LIGUE 1|SERIE A|LIGA PORTUGAL|EREDIVISIE|JUPILER PRO LEAGUE|A-LEAGUE'))]
df_filtered = df_filtered[~(df_filtered['League'].str.contains('LALIGA2|2. BUNDESLIGA|WOMEN|JUNIOREN|PLAY OFFS|RELEGATION|CUP|LIGA PORTUGAL 2'))]
df_filtered['Date'] = pd.to_datetime(df_filtered['Date'].str.replace('.', '/'), format='%d/%m/%Y').dt.date
df_filtered = df_filtered.sort_values(by=['Date', 'Country'])

# renomeando
df_odds_double = df_filtered

# ajustando nomes dos times para ficar igual ao das outras bases
df_odds_double = df_odds_double.replace({'Home' : { 'Leeds' : 'Leeds United',
                                        'Leicester' : 'Leicester City',
                                        'Wolves' : 'Wolverhampton Wanderers',
                                        'Hertha Berlin' : 'Hertha BSC',
                                        'Darmstadt' : 'Darmstadt 98',
                                        'Mainz' : 'Mainz 05',
                                        'Verona' : 'Hellas Verona',
                                        'Manchester Utd' : 'Manchester United',
                                        'AC Ajaccio' : 'Ajaccio',
                                        'B. Monchengladbach' : 'Monchengladbach',
                                        'AC Milan' : 'Milan',
                                        'Betis' : 'Real Betis',
                                        'Tottenham' : 'Tottenham Hotspur',
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Brighton' : 'Brighton and Hove Albion',
                                        'Nottingham' : 'Nottingham Forest',        
                                        'Luton' : 'Luton Town',                         
                                        'Schalke' : 'Schalke 04',
                                        'Inter' : 'Internazionale',
                                        'Ath Bilbao' : 'Athletic Club',
                                        'Cadiz CF' : 'Cadiz',
                                        'Granada CF' : 'Granada',
                                        'West Ham' : 'West Ham United',
                                        'Newcastle' : 'Newcastle United',
                                        'Clermont' : 'Clermont Foot',
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Luton' : 'Luton Town',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'PSG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Athletico Paranaense',
                                        'Vasco' : 'Vasco da Gama',
                                        'SC Farense': 'Farense',
                                        'Gil Vicente': 'Gil Vicente FC',
                                        'FC Porto': 'Porto',
                                        'FC Volendam': 'Volendam',
                                        'G.A. Eagles': 'Go Ahead Eagles',
                                        'Heracles': 'Heracles Almelo',
                                        'Nijmegen': 'NEC Nijmegen',
                                        'PSV': 'PSV Eindhoven',
                                        'Sittard': 'Fortuna Sittard',
                                        'Waalwijk': 'RKC Waalwijk',
                                        'Cercle Brugge KSV': 'Cercle Brugge',
                                        'Club Brugge KV': 'Club Brugge',
                                        'KV Mechelen': 'Mechelen',
                                        'Leuven': 'OH Leuven',
                                        'Royale Union SG': 'Union SG',
                                        'RWDM': 'RWD Molenbeek',
                                        'St. Liege': 'Standard Liege',
                                        'St. Truiden': 'Sint Truiden',
                                        'WS Wanderers': 'Western Sydney Wanderers'
                                        }})

df_odds_double = df_odds_double.replace({'Away' : { 'Leeds' : 'Leeds United',
                                        'Leicester' : 'Leicester City',
                                        'Wolves' : 'Wolverhampton Wanderers',
                                        'Hertha Berlin' : 'Hertha BSC',
                                        'Darmstadt' : 'Darmstadt 98',
                                        'Mainz' : 'Mainz 05',
                                        'Verona' : 'Hellas Verona',
                                        'Manchester Utd' : 'Manchester United',
                                        'AC Ajaccio' : 'Ajaccio',
                                        'B. Monchengladbach' : 'Monchengladbach',
                                        'AC Milan' : 'Milan',
                                        'Betis' : 'Real Betis',
                                        'Tottenham' : 'Tottenham Hotspur',
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Brighton' : 'Brighton and Hove Albion',
                                        'Nottingham' : 'Nottingham Forest',   
                                        'Luton' : 'Luton Town',                               
                                        'Schalke' : 'Schalke 04',
                                        'Inter' : 'Internazionale',
                                        'Ath Bilbao' : 'Athletic Club',
                                        'Cadiz CF' : 'Cadiz',
                                        'Granada CF' : 'Granada',
                                        'West Ham' : 'West Ham United',
                                        'Newcastle' : 'Newcastle United',
                                        'Clermont' : 'Clermont Foot',
                                        'Sheffield Utd' : 'Sheffield United',
                                        'Luton' : 'Luton Town',
                                        'Paris SG' : 'Paris Saint Germain',
                                        'PSG' : 'Paris Saint Germain',
                                        'FC Koln' : 'Koln',
                                        'AS Roma' : 'Roma',
                                        'Atl. Madrid' : 'Atletico Madrid',
                                        'Atletico-MG' : 'Atletico Mineiro',
                                        'Flamengo RJ' : 'Flamengo',
                                        'Athletico-PR' : 'Athletico Paranaense',
                                        'Vasco' : 'Vasco da Gama',
                                        'SC Farense': 'Farense',
                                        'Gil Vicente': 'Gil Vicente FC',
                                        'FC Porto': 'Porto',
                                        'FC Volendam': 'Volendam',
                                        'G.A. Eagles': 'Go Ahead Eagles',
                                        'Heracles': 'Heracles Almelo',
                                        'Nijmegen': 'NEC Nijmegen',
                                        'PSV': 'PSV Eindhoven',
                                        'Sittard': 'Fortuna Sittard',
                                        'Waalwijk': 'RKC Waalwijk',
                                        'Cercle Brugge KSV': 'Cercle Brugge',
                                        'Club Brugge KV': 'Club Brugge',
                                        'KV Mechelen': 'Mechelen',
                                        'Leuven': 'OH Leuven',
                                        'Royale Union SG': 'Union SG',
                                        'RWDM': 'RWD Molenbeek',
                                        'St. Liege': 'Standard Liege',
                                        'St. Truiden': 'Sint Truiden',
                                        'WS Wanderers': 'Western Sydney Wanderers'
                                        }})

df_odds_double = df_odds_double.reset_index()
# previsões de ml
prediction_home = []
for i in range(0, len(df_odds_double)):
    pred = ratio(df_rolling, df_odds_double['Home'][i], df_odds_double['Away'][i])
    pred['last_2_results'] = last_2_results(df_rolling, df_odds_double['Home'][i], df_odds_double['Away'][i])
    
    # Check if there are any NaN values in 'pred' DataFrame
    if pred.isnull().values.any():
        prediction = None  # Skip prediction for this row
    else:
        # Handle missing values in 'pred' DataFrame, if any
        pred.fillna(0, inplace=True)

        prediction = ml.predict_proba(pred)[0][1]
        
    prediction_home.append(prediction)

# adicionando coluna
df_odds_double['Pred_H'] = prediction_home
df_odds_double['Pred_A'] = 1 - df_odds_double['Pred_H']

# formatando
df_odds_double['Pred_H'] = df_odds_double['Pred_H'].round(2)
df_odds_double['Pred_A'] = df_odds_double['Pred_A'].round(2)

push_dataframe_to_github(df_odds_double, 'df_odds_double.csv', repository)

df_odds_final = pd.merge(df_odds, df_odds_double, on=['Home', 'Away'])[['Date_x', 'Time_x', 'Country_x', 'League_x', 'Home', 'Away', 'Odds_H', 'Odds_D', 'Odds_A', 'Odds_H_X', 'Odds_H_A', 'Odds_X_A', 'Pred_H_x', 'Pred_A_x']]

# Rename columns
new_column_names = {'Date_x': 'Date', 'Time_x': 'Time', 'Country_x': 'Country', 'League_x': 'League', 'Pred_H_x': 'Pred_H', 'Pred_A_x': 'Pred_A'}
df_odds_final.rename(columns=new_column_names, inplace=True)

#push df_odds_final to github
push_dataframe_to_github(df_odds_final, 'df_odds_final.csv', repository)