# Imports
import requests
import pandas
import numpy as np

# Get data "
Year = "2020"
CSVfile = "GiantsField"+Year+".csv"
CSVfileBat = "GiantsB"+Year+".csv"
CSVfilePitch = "GiantsP"+Year+".csv"
r = requests.get("https://www.baseball-reference.com/register/team.cgi?id=e1b4d4c9")
############################################
# Clean data [ANDY IS A FUCKING GENIOUS!]
string = r.text
string = string.replace ("-->","")
string = string.replace ("!--","")
############################################
#DF = data frame (PANDAS)
dfs = pandas.read_html(string)
# get DF 0
Bat = dfs[0]
# Dead code, but example of where clause
#Bat["Rk"] = np.where(Bat['Rk']=NaN, "TeamBat",df['Rk'])
Bat['Rk'].fillna("TeamBat", inplace=True)
Bat.sort_values(by=['BA'], ascending=True, inplace=True)
#Strip * from end of text
Bat["Name"] = Bat["Name"].str.strip("*")

Pitch = dfs[1]
Pitch['Rk'].fillna("TeamPitch", inplace=True)
#Pitch.sort_values(by=['ERA'], ascending=True, inplace=True)
#Strip * from end of text
Pitch["Name"] = Pitch["Name"].str.strip("*")


F_1B = dfs[2]
#F_1B.rename(columns={ F_1B.columns[0]: "First Base" }, inplace = True)
F_1B.loc[-1] = ["First Base",np.NaN ,np.NaN ,np.NaN ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
#F_1B.loc[0] = F_1B.style.apply('font-weight : bold')
F_1B = F_1B.sort_index(ascending=True)

F_2B = dfs[3]
#F_2B.rename(columns={ F_2B.columns[0]: "Second Base" }, inplace = True)
F_2B.loc[-1] = ["Second Base",np.NaN ,np.NaN ,np.NaN  ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
F_2B = F_2B.sort_index(ascending=True)

F_3B = dfs[4]
#F_3B.rename(columns={ F_3B.columns[0]: "Third Base" }, inplace = True)
F_3B.loc[-1] = ["Third Base",np.NaN ,np.NaN ,np.NaN  ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
F_3B = F_3B.sort_index(ascending=True)

F_SS = dfs[5]
#F_SS.rename(columns={ F_SS.columns[0]: "Short Stop" }, inplace = True)
F_SS.loc[-1] = ["Short Stop",np.NaN ,np.NaN ,np.NaN  ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
F_SS = F_SS.sort_index(ascending=True)

F_OF = dfs[6]
#F_OF.rename(columns={ F_OF.columns[0]: "Outfield" }, inplace = True)
F_OF.loc[-1] = ["Outfield",np.NaN ,np.NaN ,np.NaN  ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
F_OF = F_OF.sort_index(ascending=True)

F_Pitch = dfs[7]
#F_Pitch.rename(columns={ F_Pitch.columns[0]: "Pitching" }, inplace = True)
F_Pitch.loc[-1] = ["Pitching",np.NaN ,np.NaN ,np.NaN  ,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]
F_Pitch = F_Pitch.sort_index(ascending=True)

Fielding1 = pandas.concat([F_1B, F_2B,F_3B,F_SS, F_OF, F_Pitch], axis=1, sort=False)

Fielding = F_1B.append([F_2B,F_3B,F_SS, F_OF, F_Pitch])

# Export data
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
Fielding.to_csv(path_or_buf=CSVfile)
Bat.to_csv(path_or_buf=CSVfileBat)
Pitch.to_csv(path_or_buf=CSVfilePitch)

print("CSV Created")

#Push to Git
from git import Repo

repo_dir = 'C:/Users/Anzo'
repo = Repo(repo_dir)
file_list = CSVfile
file_list1 = CSVfileBat
file_list2 = CSVfilePitch

commit_message = 'Baseball-Reference.com'
repo.index.add(file_list)
repo.index.add(file_list1)
repo.index.add(file_list2)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

print("CSV Pushed to Github")