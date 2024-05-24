#!/usr/bin/env python
# Imports
import requests
import pandas
import numpy as np

Year = "2020"
#Git Repo directory
repo_dir = 'C:/Users/Anzo/anzodockerbuild'
##########################################################


#Japanese Source CSV
CSV_Roster = "GiantRoster"+Year+".csv"
CSV_Bat = "GiantsBat"+Year+".csv"
CSV_Pitch = "GiantsPitch"+Year+".csv"
#Baseball Reference CSV
CSV_BR_Field = "GiantsField"+Year+".csv"
CSV_BR_Bat = "GiantsB"+Year+".csv"
CSV_BR_Pitch = "GiantsP"+Year+".csv"
CSV_BR_Central = "CentralLeague"+Year+".csv"

#Data Source (Web)
r_Roster = requests.get("https://npb.jp/bis/eng/teams/rst_g.html")
r_Bat = requests.get("http://npb.jp/bis/eng/"+Year+"/stats/idb1_g.html")
r_Pitch = requests.get("http://npb.jp/bis/eng/"+Year+"/stats/idp1_g.html")
r_BR_Giants = requests.get("https://www.baseball-reference.com/register/team.cgi?id=e1b4d4c9")
r_BR_Central = requests.get("https://www.baseball-reference.com/register/league.cgi?id=4b244907")

########################################################
#Clean weird formatting in BR

string1 = r_BR_Giants.text
string1 = string1.replace ("-->","")
string1 = string1.replace ("!--","")

string2 = r_BR_Central.text
string2 = string2.replace ("-->","")
string2 = string2.replace ("!--","")
#######################################################

# BR Data Giants
dfs = pandas.read_html(string1)
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

####################################################################

# CENTRAL BR DATA
dfs2 = pandas.read_html(string2)
Standings = dfs[0]
Standings.rename(columns={ Standings.columns[0]: "Team" }, inplace = True)
Standings.rename(columns={ Standings.columns[4]: "PCT" }, inplace = True)

CentralBat = dfs2[1]
del CentralBat['Aff']
CentralBat.rename(columns={ CentralBat.columns[0]: "Team" }, inplace = True)
CentralBat.rename(columns={ CentralBat.columns[22]: "HB" }, inplace = True)

CentralPitch= dfs2[2]
del CentralPitch['Aff']
CentralPitch.rename(columns={ CentralPitch.columns[0]: "Team" }, inplace = True)
CentralPitch.rename(columns={ CentralPitch.columns[5]: "PCT" }, inplace = True)
CentralPitch.rename(columns={ CentralPitch.columns[22]: "HB" }, inplace = True)

CentralField = dfs2[3]
del CentralField['Aff']
CentralField.rename(columns={ CentralField.columns[0]: "Team" }, inplace = True)

Central = pandas.concat([CentralBat, CentralPitch, CentralField], axis=1, sort=False)


###################################################################
# Japanese Giants Pitching

dfsPitch = pandas.read_html(r_Pitch.text, header=1)

# get the first DF from the DFs
df3 = dfsPitch[0]

# Rename the handedness column
df3.rename(columns={ df3.columns[0]: "Hand" }, inplace = True)
# Rename the unamed column
df3.rename(columns={ df3.columns[12]: "PartIn" }, inplace = True)

# Manipulate data
# Replace the weird values with better stuff
df3["Hand"] = df3["Hand"].replace("*", "L")
df3["Hand"] = df3["Hand"].replace("+", "S")
df3["Hand"] = df3["Hand"].replace(np.nan, "R")

#df['random test column']=np.nan
df3.insert(0,'Last',np.nan)
df3.insert(1,'First',np.nan)
df3.insert(0,'Year',Year)
df3.insert(4,'In',np.nan)

df3[['Last','First']] = df3.Pitcher.str.split(",",expand=True)
#del df['Pitcher']
df3.rename(columns={ df3.columns[5]: 'Name' }, inplace = True)
df3['Name'] =df3['First'] + " " + df3['Last']
Newcolumn="Name"
Newcolumn2= df3.pop(Newcolumn)
df3.insert(1, Newcolumn ,Newcolumn2)

df3["First"] = df3["First"].str.strip()
df3["Name"] = df3["Name"].str.strip()
# Change part in calc
df3["PartIn"] = df3["PartIn"] * 0.3333 * 10

# Dead code, but example of where clause
# df["PartIn"] = np.where(df['PartIn']>=50, 0,df['PartIn'])

#Changing NaN to 0
df3["PartIn"].fillna(0, inplace=True)
#df["PartIn"]

# Combine innings pitched
df3["In"] = df3["IP"] + df3["PartIn"]

del df3['IP']
del df3['PartIn']
# Rename the unamed column
df3.rename(columns={ df3.columns[5]: "IP" }, inplace = True)


################################################################
# Japanese Giants Batting
dfsBat = pandas.read_html(r_Bat.text, header=1)
df4 = dfsBat[0]

# Rename the handedness column
df4.rename(columns={ df4.columns[0]: "Hand" }, inplace = True)
# Rename the unamed column


# Manipulate data
# Replace the weird values with better stuff
df4["Hand"] = df4["Hand"].replace("*", "L")
df4["Hand"] = df4["Hand"].replace("+", "S")
df4["Hand"] = df4["Hand"].replace(np.nan, "R")

#df['random test column']=np.nan
df4.insert(0,'Last',np.nan)
df4.insert(1,'First',np.nan)
df4.insert(0,'Year',Year)

df4[['Last','First']] = df4.Player.str.split(",",expand=True)
del df4['Player']
df4.rename(columns={ df4.columns[5]: 'Name' }, inplace = True)
df4['Name'] =df4['First'] + " " + df4 ['Last']
Newcolumn="Name"
Newcolumn2= df4.pop(Newcolumn)
df4.insert(1, Newcolumn ,Newcolumn2)

df4["First"] = df4["First"].str.strip()
df4["Name"] = df4["Name"].str.strip()

###################################################################
# Japanese Giants Roster

dfsroster = pandas.read_html(r_Roster.text, header=0)
# get Main Roster
df5 = dfsroster[1]

#df create new columns
df5.insert(0,'Last',np.nan)
df5.insert(1,'First',np.nan)
df5.insert(0,'Year',Year)

df5[['Last','First']] = df5.MANAGER.str.split(",",expand=True)
#del df['MANAGER']
df5["First"] = df5["First"].str.strip()

df5.rename(columns={ df5.columns[4]: 'Name' }, inplace = True)
df5['Name'] =df5['First'] + " " + df5['Last']
Newcolumn="Name"
Newcolumn2= df5.pop(Newcolumn)
df5.insert(1, Newcolumn ,Newcolumn2)

df5["Name"] = df5["Name"].str.strip()

df5.insert(4,'Bmonth',np.nan)
df5.insert(5,'Bday',np.nan)
df5.insert(6,'Byear',np.nan)

df5[['Bmonth','Byear']] = df5.Born.str.split(",",expand=True)
del df5['Born']

df5[['Bmonth','Bday']] = df5.Bmonth.str.split(" ",expand=True)
#del df['Born']

df5["Bmonth"] = df5["Bmonth"].str.strip(".")

# Rename Columns
df5.rename(columns={ df5.columns[8]: "Height (cm)" }, inplace = True)
df5.rename(columns={ df5.columns[9]: "Weight (kg)" }, inplace = True)
df5.rename(columns={ df5.columns[10]: "Throws" }, inplace = True)
df5.rename(columns={ df5.columns[11]: "Bats" }, inplace = True)
df5.rename(columns={ df5.columns[12]: "Comments" }, inplace = True)


df5Roster =df5[df5.columns[[0,1,2,3,6,4,5,7,8,9,10,11]]]

############################################################
#Create CSVs

# BR
Central.to_csv(path_or_buf=CSV_BR_Central)
Fielding.to_csv(path_or_buf=CSV_BR_Field)
Bat.to_csv(path_or_buf=CSV_BR_Bat)
Pitch.to_csv(path_or_buf=CSV_BR_Pitch)

# JAPAN
df3.to_csv(path_or_buf=CSV_Pitch)
df4.to_csv(path_or_buf=CSV_Bat)
df5Roster.to_csv(path_or_buf=CSV_Roster)
print("CSV Created")



