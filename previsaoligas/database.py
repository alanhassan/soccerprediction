import joblib
from io import BytesIO
import requests
import pandas as pd
import numpy as np

#get ml model from github

def get_ml():
    url_ml = 'https://github.com/alanhassan/soccerprediction/blob/main/best_lr.pkl?raw=true'
    file = BytesIO(requests.get(url_ml).content)
    ml = joblib.load(file)
    return ml

ml = get_ml()

ml.fitted_ = True

# updated database with recent matches from github

def get_df_rolling():
    url_df = 'https://github.com/alanhassan/soccerprediction/blob/main/df_rolling.csv?raw=true'
    data = requests.get(url_df).content
    df = pd.read_csv(BytesIO(data))

    return df

df = get_df_rolling()

# updated database with next matches and odds

def get_df_odds():
    url_df_odds = 'https://github.com/alanhassan/soccerprediction/blob/main/df_odds_final.csv?raw=true'
    data_odds = requests.get(url_df_odds).content
    df_odds = pd.read_csv(BytesIO(data_odds))
    df_odds['League'] = df_odds['League'].str.split("-").str[0]
    #df_odds['Date'] = df_odds['Date'].dt.date
    df_odds = df_odds.sort_values(by=['Date', 'Country'])
    # Update 'League' values based on 'Country'
    df_odds.loc[df_odds['Country'] == 'GERMANY', 'League'] = 'Alemanha - Bundesliga'
    df_odds.loc[df_odds['Country'] == 'AUSTRALIA', 'League'] = 'Austrália - A-League'
    df_odds.loc[df_odds['Country'] == 'BELGIUM', 'League'] = 'Bélgica - Pro League A'
    df_odds.loc[df_odds['Country'] == 'BRAZIL', 'League'] = 'Brasil - Série A'
    df_odds.loc[df_odds['Country'] == 'SPAIN', 'League'] = 'Espanha - La Liga'
    df_odds.loc[df_odds['Country'] == 'FRANCE', 'League'] = 'França - Ligue 1'
    df_odds.loc[df_odds['Country'] == 'NETHERLANDS', 'League'] = 'Holanda - Eredivisie'
    df_odds.loc[df_odds['Country'] == 'ENGLAND', 'League'] = 'Inglaterra - Premier League'
    df_odds.loc[df_odds['Country'] == 'ITALY', 'League'] = 'Itália - Serie A'
    df_odds.loc[df_odds['Country'] == 'PORTUGAL', 'League'] = 'Portugal - Primeira Liga'
    df_odds = df_odds.sort_values('League')
    df_odds = df_odds[['Date', 'League', 'Home', 'Away', 'Odds_H', 'Odds_D', 'Odds_A', 'Odds_H_X', 'Odds_H_A', 'Odds_X_A', 'Pred_H', 'Pred_A']]
    df_odds = df_odds.rename(columns={"Date": "Data", "League": "Campeonato",
                                      "Home": "Time CASA", 'Away': "time VISITANTE",
                                      "Odds_H": "Odds 1", "Odds_D": "Odds X",
                                      "Odds_A": "Odds 2",
                                      "Odds_H_X": "Odds 1X" ,"Odds_H_A": "Odds 12",
                                      "Odds_X_A": "Odds X2", "Pred_H": "Previsão 1",
                                      "Pred_A": "Previsão 2"})
    df_odds['Dica'] = np.where(
    ((df_odds['Previsão 1'] >= 0.80) & (df_odds['Odds 1'] >= 1.20) & (df_odds['Odds 1'] <= 1.90)) |
    ((df_odds['Previsão 2'] >= 0.65) & (df_odds['Odds 2'] >= 1.20) & (df_odds['Odds 2'] <= 1.75)),
    'Sim',  # Value if True
    'Não'   # Value if False
)
    return df_odds

df_odds = get_df_odds()

# get information for 'last_2_results_sum'

def get_match_df_final_all():
    url_match_df_final_all = 'https://github.com/alanhassan/soccerprediction/blob/main/match_df_final_all.csv?raw=true'
    df_match_df_final_all = requests.get(url_match_df_final_all).content
    match_df_final_all = pd.read_csv(BytesIO(df_match_df_final_all))
    
    return match_df_final_all

match_df_final_all = get_match_df_final_all()

# get information for 'tips_original_result'

tips_original_result = 'https://github.com/alanhassan/soccerprediction/blob/main/tips_original_result.csv?raw=true'
tips_original_result = requests.get(tips_original_result).content
tips_original_result = pd.read_csv(BytesIO(tips_original_result))

# func home
def homeData(df, team):
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
def awayData(df, team):
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
    df = homeData(df, f'{team1}')/awayData(df, f'{team2}')
    df.rename(columns={"Points last season": "points_last_season_ratio",
                        "pont_rolling": "pont_rolling_ratio",
                        "gf_rolling": "gf_rolling_ratio",
                        "ga_rolling": "ga_rolling_ratio"}, inplace=True)
    return df

# func for 'last_2_results'
def last_2_results(team1, team2):
    df = match_df_final_all.sort_values(by='date').reset_index(drop=True)
    length = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].shape[0]
    if length >= 2:
        last_2_results_sum = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].iloc[-1]['last_2_results_sum']
    elif length == 1:
        last_2_results_sum = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].iloc[-1]['pont']
    elif length == 0:
        last_2_results_sum = 1
    return last_2_results_sum

# func for 'last_2_results' text on streamlit
def last_results_text_home(team1, team2):
    df = match_df_final_all.sort_values(by='date').reset_index(drop=True)
    length = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].shape[0]
    last = []
    for i in range(1,length+1):
        x = df[(df['team'] == f'{team1}') & (df['opponent'] == f'{team2}')].iloc[-i]['result']
        last.append(x)
    return str(last)[1:-1]


# func for 'last_2_results' text on streamlit
def last_results_text_away(team1, team2):
    df = match_df_final_all.sort_values(by='date').reset_index(drop=True)
    length = df[(df['team'] == f'{team2}') & (df['opponent'] == f'{team1}')].shape[0]
    last = []
    for i in range(1, length+1):
        x = df[(df['team'] == f'{team2}') & (df['opponent'] == f'{team1}')].iloc[-i]['result']
        last.append(x)
    return str(last)[1:-1]


def ml_pred(team1, team2):
    pred = ratio(df, team1, team2)
    pred['last_2_results'] = last_2_results(team1, team2)
    prediction = ml.predict_proba(pred)[0][1]
    return prediction