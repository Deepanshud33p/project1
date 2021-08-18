#!/usr/bin/env python
# coding: utf-8

# In[2]:


import warnings
warnings.filterwarnings('ignore')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
get_ipython().run_line_magic('matplotlib', 'inline')

bowler_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\Bowler_data.csv')
ground_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\Ground_Averages.csv')
odi_result_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\ODI_Match_Results.csv')
odi_scores_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\ODI_Match_Totals.csv')
players_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\WC_players.csv')


# In[3]:


#gives better understanding than odi_result_data
odi_scores_data.head()


# In[4]:


odi_scores_data=odi_scores_data.rename(columns={'Unnamed: 0':'scores_id'})
odi_scores_data.head()


# In[5]:


odi_scores_data.Ground


# In[6]:


WC_venue_pitches = ["The Oval, London","Trent Bridge, Nottingham","Sophia Gardens, Cardiff","County Ground, Bristol","Rose Bowl, Southampton","County Ground, Taunton","Old Trafford, Manchester","Edgbaston, Birmingham","Headingley, Leeds","Lord's, London","Riverside Ground, Chester-le-Street"]
wc_grounds = []
odi_grounds = odi_scores_data.Ground
for i in odi_grounds:
    for j in WC_venue_pitches:
        if i in j :
            
            wc_grounds.append((i,j))


# In[7]:


wc_grounds


# In[8]:


Ground_names = dict(set(wc_grounds))
def Full_Ground_names(value):
    return Ground_names[value]
Ground_names


# In[9]:


#Let's gather the data of all ODI's in these WC Venues
WC_Grounds_History = odi_scores_data[odi_scores_data.Ground.isin(Ground_names.keys())]


WC_Grounds_History['Ground']= WC_Grounds_History.Ground.apply(Full_Ground_names)
WC_Grounds_History.head()


# In[10]:


Team_matches=WC_Grounds_History.Country.value_counts().reset_index()
Team_matches.head()


# In[11]:


sns.barplot(x="index",y="Country",data=Team_matches).set_title('Number of Matches played by each Country at these Venues')
plt.xlabel('Countries')
plt.ylabel(' Matches played')
plt.xticks(rotation=60)


# In[12]:


#this shows england had the upper hand at these Venues,they are more used to the pitches condition .


# In[13]:



WC_Grounds_History.sample(6)
WC_Grounds_History.Result.value_counts()


# In[14]:


WC_Grounds_History = WC_Grounds_History[~WC_Grounds_History.Result.isin(["-"])]
WC_Grounds_History.Result.value_counts()


# In[15]:


winnings = WC_Grounds_History[["Country","Result"]]
winnings["count"] = 1
Ground_Results_Per_Team = winnings.groupby(["Country","Result"]).sum()
Ground_Results_Per_Team 
#here Result column  is the first level of hierarchy so we will apply level=0 for calculating result percentage of each country


# In[16]:


Ground_Results_Per_Team = Ground_Results_Per_Team.groupby(level=0).apply(lambda x:100 * x / float(x.sum())).reset_index()
Ground_Results_Per_Team.columns = ["Country","Result","Count"]
Ground_Results_Per_Team.head()


# In[17]:


#now creating a barplot representing the results of each country
plt.figure(figsize=(15,8))
sns.barplot(x = "Country", y = "Count", hue = "Result", data = Ground_Results_Per_Team)
plt.ylabel("Percentage")
plt.title("Country - Results")
plt.xticks(rotation = 60)


# In[18]:


#as we can see here India and England have  the highest winning percentage 
#where Westindies and South Africa having the highest losing percentage
#lets see when India and England face off each other
India_vs_England = WC_Grounds_History[WC_Grounds_History.Country == "England"][WC_Grounds_History.Opposition.str.contains("India")]
India_vs_England = India_vs_England.Result.value_counts().reset_index()
India_vs_England


# In[19]:


sns.barplot(x="index",y="Result",data=India_vs_England)
plt.xlabel('England')


# In[20]:


Inning_Wins = WC_Grounds_History[WC_Grounds_History.Result == "won"].Inns.value_counts(normalize = True).reset_index()
Inning_Wins
normalize = True
sns.barplot(x = "index", y = "Inns", data = Inning_Wins).set_title("Winnings by Innings")
plt.xlabel("Innings")
plt.ylabel("Winning Percentage")


# In[21]:


#this shows  that the team who bowls first have the  approx. 57% chances of winning
WC_Grounds_History.sample(5)
                         


# In[22]:


pitch_innings=WC_Grounds_History[WC_Grounds_History.Result=="won"][["Inns","Ground"]]
pitch_innings["count"]=1
pitch_innings = pitch_innings.groupby(["Ground","Inns"]).sum()
pitch_innings=pitch_innings.groupby(level=0).apply(lambda x: 100*x/float(x.sum())).reset_index()
pitch_innings.head()


# In[23]:


plt.figure(figsize=(10,10))
sns.barplot(x="Ground",y="count",hue="Inns",data=pitch_innings).set_title('win percent in grounds by innings')
plt.xticks(rotation=60)
plt.ylabel('win precentage')


# In[24]:


WC_Grounds_History=WC_Grounds_History[~WC_Grounds_History.Score.str.contains('D')]
#WC_Grounds_History.head()
splited_scores=[int(i[0]) for i in WC_Grounds_History.Score.str.split('/')]
WC_Grounds_History['OnlyScores'] =splited_scores
Stadium_scores=WC_Grounds_History[["OnlyScores","Ground"]]
Stadium_scores=Stadium_scores[Stadium_scores.OnlyScores>50]
#Stadium_scores.head()
plt.figure(figsize=(15,8))
plt.xticks(rotation =60)
sns.violinplot(x="Ground",y="OnlyScores",  data=Stadium_scores).set_title('Scores VS Pitches')
#from the violinplot, it is clear that 


# In[25]:


def no_of_wickets(value):
    if "/" not in value:
        return 10
    elif "D" in value:
        return 0
    else:
        return int(value.split("/")[-1])
WC_Grounds_History["Total_Wickets"] = WC_Grounds_History.Score.apply(no_of_wickets)
WC_Grounds_History.head()


# In[26]:


Stadium_Wickets = WC_Grounds_History[["Total_Wickets","Ground"]]
Stadium_Wickets = Stadium_Wickets.groupby("Ground").mean().reset_index()
Stadium_Wickets.head()


# In[27]:


plt.figure(figsize=(15,8))
plt.xticks(rotation=60)
sns.barplot(x="Ground",y="Total_Wickets",data=Stadium_Wickets)
#as we can see here avearge wickets per ground is 6-7


# # Let's analyze the batsmen_data

# In[28]:


batsmen_data=pd.read_csv(r'C:\Users\acer\Desktop\sample_datasets\Batsman_data.csv')

batsmen_data.drop(columns=batsmen_data.columns[0],inplace=True)
#batsmen_data.head()
batsmen_data=batsmen_data[~batsmen_data.Bat1.isin(["DNB","TDNB"])]
batsmen_data=batsmen_data[batsmen_data.Player_ID.isin(players_data.ID)]
stadiums=[i for i in Ground_names.keys()]

batsmen_data_in_england=batsmen_data[batsmen_data.Ground.isin(stadiums)]
#batsmen_data_in_england=batsmen_data_in_england.Ground.apply(Full_Ground_names)
batsmen_data_in_england["Ground"]=batsmen_data_in_england.Ground.apply(Full_Ground_names)
batsmen_data_in_england


# In[29]:


#for finding averages of batsmen
def times_out(value):
    if "*" in value:
        return 0
    else:
        return 1

batsmen_data_in_england["Times_out"]=batsmen_data_in_england.Bat1.apply(times_out)  
change_type=["Runs","BF","4s","6s"]
for i in change_type:
    batsmen_data_in_england[i]=batsmen_data_in_england[i].astype("int")

batsmen_data_in_england.sample(10)


# In[30]:


#batsmen_data_in_england.groupby(["Ground","Batsman"]).sum()


# In[31]:


batsmen_data_in_england=batsmen_data_in_england.groupby(["Ground","Batsman"]).sum().reset_index()
batsmen_data_in_england["average"]=batsmen_data_in_england["Runs"]/batsmen_data_in_england["Times_out"]

batsmen_data_in_england.sample(25)


# In[32]:


batsmen_scores=batsmen_data_in_england.groupby(['Batsman']).sum().reset_index()
batsmen_scores["Average"]=batsmen_scores["Runs"]/batsmen_scores["Times_out"]

#batsmen_scores=batsmen_scores.drop(['average'],axis=1,inplace=True)
batsmen_scores.sort_values(by="Average",ascending=False).sample(5)


# In[33]:


batsmen_scores.drop(columns="average",inplace=True)


# In[34]:


best_batsmen_avg=batsmen_scores[(batsmen_scores.Times_out>0) &(batsmen_scores.Average>40)].sort_values(by="Average",ascending=False)
best_batsmen_avg


# In[35]:


Player_Name_Id=batsmen_data[["Player_ID","Batsman"]].drop_duplicates()


# In[36]:


Player_id=list(best_batsmen_avg.merge(Player_Name_Id,how="left",on="Batsman")["Player_ID_y"].astype("int"))


# In[37]:


best_batsmen_avg["Player_ID"]=Player_id
best_batsmen_avg


# In[38]:


players_data.sample(6)


# In[39]:


players_data.columns=["Player","Player_ID","Country"]
#players_data.sample(6)
Country_Player=list(best_batsmen_avg.merge(players_data,how = "left",on="Player_ID")["Country"])
best_batsmen_avg["Country"]=Country_Player
best_batsmen_avg.head()


# In[40]:


sns.countplot(best_batsmen_avg["Country"]).set_title("No.of Best Batsman per Team")
plt.xticks(rotation = 60)


# In[41]:


best_batsmen_avg["Strike_Rate"]=best_batsmen_avg["Runs"]/best_batsmen_avg["BF"]*100
best_batsmen_avg.sort_values(["Strike_Rate"],ascending=False).head(10)


# # Now moving onto to bowler's data and analyze it :)

# In[82]:


for i in Ground_names.keys():
       print(i,end= '  ')
       
       
stadiums       


# In[83]:


bowler_data.head(15)


# In[84]:


bowler_data=bowler_data[bowler_data.Ground.isin(stadiums)]
bowler_data=bowler_data[~bowler_data.Overs.str.contains('-')]
bowler_data.head(10)


# Econ : Economy of Bowler means, how many runs does the Bowler concede in one Over?
# Ave : Average for a Bowler means, how many runs conceded by Bowler per wicket.
# SR : Strike Rate refers to no.of balls bowled for gaining the wicket.
# Mdns : Maiden Over refers that the Bowler didn't concede any run.

# In[85]:


#now for calculating no. of balls ,we will create a function def total_balls
def total_balls(value):
    if '.' in value:
        over= value.split('.')
        return int(over[0])*6 + int(over[1])
    else:
        return int(value)*6
    
bowler_data["Total_balls"]=bowler_data.Overs.apply(total_balls) 
bowler_data.head(15)


# In[86]:


samp=["Overs","Runs","Total_balls","Wkts"]
for i in samp:
    bowler_data[i]=bowler_data[i].astype("float")
#bowler_data.head(8) 
#bowler_data.Ground=bowler_data.Ground.apply(Full_Ground_names)
#bowler_data.head(8)
bowler_data_england=bowler_data.groupby("Bowler").sum().reset_index()
bowler_data_england


# In[87]:


bowler_data_england['Bowling_Econ.']=bowler_data_england["Runs"]/bowler_data_england["Overs"]
bowler_data_england['Bowling_S.R']=bowler_data_england["Total_balls"]/bowler_data_england["Wkts"]
bowler_data_england['Bowling_Avg']=bowler_data_england["Runs"]/bowler_data_england['Wkts']
bowler_data_england


# In[88]:


bowler_data_england[bowler_data_england.Bowler==('Jasprit Bumrah')]


# In[89]:


bowler_data_england=bowler_data_england[(bowler_data_england.Overs>9)&(bowler_data_england.Wkts>0)]
bowler_data_england


# In[107]:


bowler_data_england.head(10)


# In[108]:


Player_WC_ID = bowler_data[["Player_ID","Bowler"]].drop_duplicates()
Player_WC_ID


# In[109]:


bowler_data_england=bowler_data_england.merge(Player_WC_ID,how = "left",on = "Bowler")
bowler_data_england


# In[112]:



#players_data.sample(10)
country=list(bowler_data_england.merge(players_data,how = "left",on = "Player_ID")["Country"])

bowler_data_england["Country"]=country


# In[113]:


bowler_data_england=bowler_data_england.drop(['Player_ID_x','Player_ID'],axis=1)
bowler_data_england


# In[114]:


bowler_data_england=bowler_data_england.rename(columns={'Player_ID_y':'Player_ID'})
bowler_data_england

