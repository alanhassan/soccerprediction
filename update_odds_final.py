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

warnings.filterwarnings("ignore")

# conectando com github

#token

key = os.environ.get('API_Key')
g = Github(key)

#repositório
repo = g.get_repo("alanhassan/soccerprediction")

df_odds = pd.read_excel('df_odds.xlsx')
df_odds_double = pd.read_excel('df_odds_double.xlsx')

print('oi')

df_odds_final = pd.merge(df_odds, df_odds_double, on=['Date', 'Home', 'Away'])[['Date', 'Time_x', 'Country_x', 'League_x', 'Home', 'Away', 'Odds_H', 'Odds_D', 'Odds_A', 'Odds_H_X', 'Odds_H_A', 'Odds_X_A', 'Pred_H_x', 'Pred_A_x']]

# Rename columns
new_column_names = {'Time_x': 'Time', 'Country_x': 'Country', 'League_x': 'League', 'Pred_H_x': 'Pred_H', 'Pred_A_x': 'Pred_A'}
df_odds_final.rename(columns=new_column_names, inplace=True)

# Gerando os dados para excel
df_odds_final.to_excel('C:/Users/alan.hassan/Desktop/github/soccerprediction/df_odds_final.xlsx')

# update no Github
repo = Repo('C:/Users/alan.hassan/Desktop/github/soccerprediction')  # if repo is CWD just do '.'
origin = repo.remote('origin')

assert origin.exists()
origin.fetch()
repo.git.pull('origin','main')
repo.index.add('df_odds_final.xlsx')
repo.index.commit("your commit message")
repo.git.push("--set-upstream", origin, repo.head.ref)
