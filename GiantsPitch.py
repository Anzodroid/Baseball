#!/usr/bin/env python
# Imports
import requests
import pandas
import numpy as np
# import github
#import gitpython
# import git
# The OS module in python provides functions for interacting with the operating system. .
import os



# Get data
# Source: http://npb.jp/bis/eng/2019/stats/idb1_g.html
Year = "2020"
CSVfile = "GiantsPitch"+Year+".csv"
r = requests.get("http://npb.jp/bis/eng/"+Year+"/stats/idp1_g.html")

# Clean data
#DF = data frame (PANDAS)

# Function https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.read_html.html
dfs = pandas.read_html(r.text, header=1)

# get the first DF from the DFs
df = dfs[0]

# Rename the handedness column
df.rename(columns={ df.columns[0]: "Hand" }, inplace = True)
# Rename the unamed column
df.rename(columns={ df.columns[12]: "PartIn" }, inplace = True)

# Manipulate data
# Replace the weird values with better stuff
df["Hand"] = df["Hand"].replace("*", "L")
df["Hand"] = df["Hand"].replace("+", "S")
df["Hand"] = df["Hand"].replace(np.nan, "R")

#df['random test column']=np.nan
df.insert(0,'Last',np.nan)
df.insert(1,'First',np.nan)
df.insert(0,'Year',Year)
df.insert(4,'In',np.nan)

df[['Last','First']] = df.Pitcher.str.split(",",expand=True)
#del df['Pitcher']
df.rename(columns={ df.columns[5]: 'Name' }, inplace = True)
df['Name'] =df['First'] + " " + df ['Last']
Newcolumn="Name"
Newcolumn2= df.pop(Newcolumn)
df.insert(1, Newcolumn ,Newcolumn2)

df["First"] = df["First"].str.strip()
df["Name"] = df["Name"].str.strip()
# Change part in calc
df["PartIn"] = df["PartIn"] * 0.3333 * 10

# Dead code, but example of where clause
# df["PartIn"] = np.where(df['PartIn']>=50, 0,df['PartIn'])

#Changing NaN to 0
df["PartIn"].fillna(0, inplace=True)
#df["PartIn"]

# Combine innings pitched
df["In"] = df["IP"] + df["PartIn"]

del df['IP']
del df['PartIn']
# Rename the unamed column
df.rename(columns={ df.columns[5]: "IP" }, inplace = True)

# Export data
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
df.to_csv(path_or_buf=CSVfile)
print("CSV Created")
##################################################################


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
