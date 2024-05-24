# Imports

import requests
import pandas
import numpy as np

# Get data "https://npb.jp/bis/eng/teams/rst_g.html#pit"
Year = "2020"
CSVfile = "GiantRoster"+Year+".csv"
r = requests.get("https://npb.jp/bis/eng/teams/rst_g.html#pit")

# Clean data
#DF = data frame (PANDAS)
# Function https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html
dfs = pandas.read_html(r.text, header=0)
# get Main Roster
df = dfs[1]

#df create new columns
df.insert(0,'Last',np.nan)
df.insert(1,'First',np.nan)
df.insert(0,'Year',Year)

df[['Last','First']] = df.MANAGER.str.split(",",expand=True)
#del df['MANAGER']
df["First"] = df["First"].str.strip()

df.rename(columns={ df.columns[4]: 'Name' }, inplace = True)
df['Name'] =df['First'] + " " + df ['Last']
Newcolumn="Name"
Newcolumn2= df.pop(Newcolumn)
df.insert(1, Newcolumn ,Newcolumn2)

df["Name"] = df["Name"].str.strip()

df.insert(4,'Bmonth',np.nan)
df.insert(5,'Bday',np.nan)
df.insert(6,'Byear',np.nan)

df[['Bmonth','Byear']] = df.Born.str.split(",",expand=True)
del df['Born']

df[['Bmonth','Bday']] = df.Bmonth.str.split(" ",expand=True)
#del df['Born']

df["Bmonth"] = df["Bmonth"].str.strip(".")

# Rename Columns
df.rename(columns={ df.columns[8]: "Height (cm)" }, inplace = True)
df.rename(columns={ df.columns[9]: "Weight (kg)" }, inplace = True)
df.rename(columns={ df.columns[10]: "Throws" }, inplace = True)
df.rename(columns={ df.columns[11]: "Bats" }, inplace = True)
df.rename(columns={ df.columns[12]: "Comments" }, inplace = True)


df2=df[df.columns[[0,1,2,3,6,4,5,7,8,9,10,11]]]
print(df2)
# Export data
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
df2.to_csv(path_or_buf=CSVfile)
print("CSV Created")

#Push to Git
from git import Repo

repo_dir = 'C:/Users/Anzo'
repo = Repo(repo_dir)
file_list = CSVfile

commit_message = 'NPB Website'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

print("CSV Pushed to Github")