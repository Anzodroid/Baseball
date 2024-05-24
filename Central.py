# Imports
import requests
import pandas
import numpy as np

# Get data "
Year = "2020"
CSVfile = "CentralLeague"+Year+".csv"
r = requests.get("https://www.baseball-reference.com/register/league.cgi?id=4b244907")
############################################
# Clean data [ANDY IS A FUCKING GENIOUS!]
string = r.text
string = string.replace ("-->","")
string = string.replace ("!--","")
############################################

dfs = pandas.read_html(string)
# get DF 0
Standings = dfs[0]
Standings.rename(columns={ Standings.columns[0]: "Team" }, inplace = True)
Standings.rename(columns={ Standings.columns[4]: "PCT" }, inplace = True)

CentralBat = dfs[1]
del CentralBat['Aff']
CentralBat.rename(columns={ CentralBat.columns[0]: "Team" }, inplace = True)
CentralBat.rename(columns={ CentralBat.columns[22]: "HB" }, inplace = True)

CentralPitch= dfs[2]
del CentralPitch['Aff']
CentralPitch.rename(columns={ CentralPitch.columns[0]: "Team" }, inplace = True)
CentralPitch.rename(columns={ CentralPitch.columns[5]: "PCT" }, inplace = True)
CentralPitch.rename(columns={ CentralPitch.columns[22]: "HB" }, inplace = True)

CentralField = dfs[3]
del CentralField['Aff']
CentralField.rename(columns={ CentralField.columns[0]: "Team" }, inplace = True)

Concat = pandas.concat([CentralBat, CentralPitch, CentralField], axis=1, sort=False)

# Export data
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
Concat.to_csv(path_or_buf=CSVfile)

print("CSV Created")

#Push to Git
from git import Repo

repo_dir = 'C:/Users/Anzo'
repo = Repo(repo_dir)
file_list = CSVfile

commit_message = 'Baseball-Reference.com'
repo.index.add(file_list)

repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

print("CSV Pushed to Github")