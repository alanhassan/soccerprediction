import requests
import pandas as pd
import numpy as np
import warnings
from git import Repo
from io import StringIO
import creds
import base64
from io import BytesIO


warnings.filterwarnings("ignore")



# get data

url_df_odds = 'https://github.com/alanhassan/soccerprediction/blob/main/df_odds_final.csv?raw=true'
data_odds = requests.get(url_df_odds).content
df_odds = pd.read_csv(BytesIO(data_odds))
df_odds['League'] = df_odds['League'].str.split("-").str[0]
#df_odds['Date'] = df_odds['Date'].dt.date
df_odds = df_odds.sort_values(by=['Date', 'Country'])
df_odds['Date'] = df_odds['Date'].astype(str)
df_odds = df_odds[['Date', 'League', 'Home', 'Away', 'Odds_H', 'Odds_D', 'Odds_A', 'Odds_H_X', 'Odds_H_A', 'Odds_X_A', 'Pred_H', 'Pred_A']]

# Selecionando as partidas boas para apostar e adicionando colunas

# Bets that pay more than 1.4, and have more than 80% prob of being right

safest_bet = df_odds[((df_odds['Pred_H'] >= 0.80) & ((df_odds['Odds_H'] >= 1.20) & (df_odds['Odds_H'] <= 1.90))) | ((df_odds['Pred_A'] >= 0.65) & ((df_odds['Odds_A'] >= 1.20) & (df_odds['Odds_A'] <= 1.75)))]
if safest_bet.empty:
    print('Filtered dataframe is empty')
else:
    safest_bet['Winning_team'] = safest_bet.apply(lambda x: x['Home'] if x['Pred_H'] > x['Pred_A'] else x['Away'], axis=1)
    safest_bet['Winning_prob'] = safest_bet.apply(lambda x: x['Pred_H'] if x['Pred_H'] > x['Pred_A'] else x['Pred_A'], axis=1)
    safest_bet['Winning_bet'] = safest_bet.apply(lambda x: x['Odds_H'] if x['Pred_H'] > x['Pred_A'] else x['Odds_A'], axis=1)
    safest_bet['Winning_bet_final'] =  safest_bet.apply(lambda x: x['Odds_H_X'] if (x['Winning_bet'] >= 1.60 and x['Pred_H'] > x['Pred_A'] and x['Winning_prob'] < 0.85) else (x['Odds_X_A'] if (x['Winning_bet'] >= 1.60 and x['Pred_A'] > x['Pred_H'] and x['Winning_prob'] < 0.85) else x['Winning_bet']),
    axis=1
)
    safest_bet['bet_type'] = 'safest_bet'
    safest_bet['bet_type_order'] = 3


new_tips = safest_bet
# drop duplicates, keeping the first occurrence of each row (according to the order of importance)
if new_tips.empty:
    print('Filtered dataframe is empty')
else:
    new_tips = new_tips.sort_values("bet_type_order", ascending=False).drop_duplicates(subset=new_tips.columns[:-2], keep="first")

#new_tips.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/new_tips.xlsx')

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
push_dataframe_to_github(new_tips, 'new_tips.csv', repository)

# load tips_original.xlsx

url_tips_original = 'https://github.com/alanhassan/soccerprediction/blob/main/tips_original.csv?raw=true'
data = requests.get(url_tips_original).content
tips_original = pd.read_csv(BytesIO(data))

tips_original = tips_original[['Date', 'League', 'Home', 'Away',
                                'Odds_H', 'Odds_A', 'Odds_H_X', 'Odds_X_A', 'Pred_H', 'Pred_A', 'Winning_team',
                                'Winning_prob', 'Winning_bet', 'Winning_bet_final', 'bet_type', 'bet_type_order']]


# append the new rows to tips_original dataframe
if new_tips.empty:
    tips_original = tips_original
else:
    tips_original = pd.concat([tips_original, new_tips])


# remove duplicated rows

tips_original = tips_original[['Date', 'League', 'Home', 'Away',
                                'Odds_H', 'Odds_A', 'Odds_H_X', 'Odds_X_A', 'Pred_H', 'Pred_A', 'Winning_team',
                                'Winning_prob', 'Winning_bet', 'Winning_bet_final', 'bet_type', 'bet_type_order']].drop_duplicates()

# # save new df of tips_original

# tips_original.to_sql('tips_original', engine, if_exists='replace', index=False)

# update no Github
push_dataframe_to_github(tips_original, 'tips_original.csv', repository)

# Get the results of the matches that have already happened

match_df_final_all = 'https://github.com/alanhassan/soccerprediction/blob/main/match_df_final_all.csv?raw=true'
data = requests.get(match_df_final_all).content
match_df_final_all = pd.read_csv(BytesIO(data))

# convert the 'date' column to object type
match_df_final_all['date'] = match_df_final_all['date'].astype(str)

# merge with tips_original
tips_original_result = pd.merge(tips_original, match_df_final_all[['date', 'team', 'opponent', 'result']], left_on=['Date', 'Home', 'Away'], right_on=['date', 'team', 'opponent'], how='inner')

# Add column with the team that won

tips_original_result['Winning_team_actual'] = np.where(tips_original_result['result'] == 'L', tips_original_result['opponent'],
                                     np.where(tips_original_result['result'] == 'D', 'Draw', tips_original_result['team']))


# Adding columns of bet is right 

tips_original_result['bet_right'] = np.where(
    ((tips_original_result['Winning_team_actual'] == tips_original_result['Winning_team']) | 
    ((tips_original_result['result'] == 'D') & (tips_original_result['Winning_bet'] >= 1.60) & (tips_original_result['Winning_prob'] <= 0.85))),
    1,
    0
)

# Adding columns of bet is right (win or draw)

tips_original_result['bet_right_win_draw'] = np.where(tips_original_result['Winning_team_actual'] == tips_original_result['Winning_team'], 1,
                                     np.where(tips_original_result['Winning_team_actual'] == 'Draw', 1, 0))

# Removing duplicated rows
tips_original_result = tips_original_result.drop_duplicates(subset=['Date', 'League', 'Home', 'Away'], keep='first')

# #saving file
# tips_original_result.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/tips_original_result.xlsx')

# update no Github
push_dataframe_to_github(tips_original_result, 'tips_original_result.csv', repository)
