import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns 

data = pd.read_csv('./out.csv')
links = pd.read_csv('./links.csv')

df = pd.DataFrame(data)
df['nationality'] = df['nationality'].astype('string')
ndf=df.dropna(subset=['nationality'])
ndf2=ndf.dropna(subset=['pro-matches-winrate'])
cleanDf=ndf2.dropna(subset=['age'])


# Is there a correlation between versing a diverse pool of opponents and a player's win rate?

#get the number of players a player has played with that has UNIQUE natinality and or age 
#number of links with unique attributes ^
rowID = 0
diversityCount = []
while rowID<1021: #cleanDf has 1021 rows :(
    row = cleanDf.iloc[rowID]
    nodeLinks =links.loc[links['Source'] == rowID]
    targetNodes = nodeLinks['Target']
    numberOfTargets = len(targetNodes)

    targetRowID = 0
    linkAttributes = []
    uniqueLinkAttributesCount = 0
    while targetRowID<numberOfTargets:
        targetAttributes = cleanDf.iloc[targetRowID]
        targetAge = targetAttributes['age']
        targetNat = targetAttributes['nationality']
        linkAttributes.append(targetAge)
        linkAttributes.append(targetNat)
        uniqueLinkAttributes = set(linkAttributes)
        uniqueLinkAttributesCount = len(uniqueLinkAttributes)
        targetRowID+=1
    
    diversityCount.append(uniqueLinkAttributesCount)
   
    rowID+=1




i = 0
dictLength = len(diversityCount)
#calc avg winrate for each diversity count 
uniqueDiversityCounts = set(diversityCount)
# print(uniqueDiversityCounts)

diversityWinrate = {}

while i<dictLength:
    diversityWinrate[i]={
                    'winrate': cleanDf.iloc[i]['pro-matches-winrate'], 
                    'diversityCount': diversityCount[i],
                    }
    # diversityWinrate[i] = 
    i+=1
diversityDf = pd.DataFrame.from_dict(diversityWinrate,orient='index')
i=0
uniqueDiversityCountsSORTED = sorted(uniqueDiversityCounts)
while i<len(uniqueDiversityCounts):
    currDiversityCount = uniqueDiversityCounts.pop()
    dCDf = diversityDf.loc[diversityDf['diversityCount'] == currDiversityCount]
    pp = dCDf.groupby("diversityCount")
    mean = pp.mean()

    i+=1



pp = diversityDf.groupby(['diversityCount']).mean()
counts = diversityDf.groupby(['diversityCount']).count()
count = counts.rename(columns={'winrate' : 'Number of Players With Same Diversity Count'})

print(pp)

# ax = sns.scatterplot(x=pp['winrate'],y=uniqueDiversityCountsSORTED, size=count['Number of Players With Same Diversity Count'])
# ax.set(
#         xlabel = 'Mean Win Rate Among Players With Same Diversity Count',
#         ylabel = 'Diversity Count',
#         title = 'Correlation Between Playing Against A Diverse Number of Oppenents and Win Rate'
#     )
# plt.figure(figsize=(10, 10), dpi=80)
# plt.scatter(pp['winrate'], uniqueDiversityCountsSORTED)
# plt.xlabel("Player Win Rate (Match Wins/Total Matches)")
# plt.ylabel("Number of Diverse Opponents")
# plt.savefig('winrateAndOpponentDiversity.png')
# plt.show()

# def getDuplicateSizes(df,sortedDf):
#     i = 0
#     duplicateCount = []

#     while (i<len(df)):
        





# How does a player's age & nationality affect their win rate?
def plotAgeAndWinrate():
    # print(cleanDf)
    pp = cleanDf[['age','pro-matches-winrate']]
    noRanges = pp[cleanDf['age'].str.contains('-') == False ]
    countOfPlayersInAgeRange = noRanges.groupby(['age']).count()
    count = countOfPlayersInAgeRange.rename(columns={'pro-matches-winrate' : 'Number of Players In Age Group'})
    sortedCount = count.sort_index(ascending=False)
    print(sortedCount)
    sortedCount.to_csv('ageCountscsv.csv')
    avgWinratePerAge = noRanges.groupby(['age']).mean()
    
    sortedDf = avgWinratePerAge.sort_values(by=['age'],ascending=False)
    sortedAges = sorted(set(noRanges['age']), reverse = True)

    ax = sns.scatterplot(x = sortedDf['pro-matches-winrate'], y=sortedAges, size = sortedCount['Number of Players In Age Group'] )
    ax.set(
        xlabel = 'Mean Win Rate Within Age Group',
        ylabel = 'Age Group',
        title = 'Correlation Between Age and Win Rate'
    )
    plt.show()
    # plt.figure(figsize=(10, 10), dpi=80)
    # plt.scatter( sortedDf['pro-matches-winrate'],sortedAges)
    plt.xlabel("Player Win Rate (Match Wins/Total Matches)")
    plt.ylabel("Player age")
    plt.title("Correlation Between Player Age and Winrate")
    # plt.show()
    # a, b = np.polyfit(sortedDf['pro-matches-winrate'], sortedDf['age'], 1)
    # plt.plot(sortedDf['pro-matches-winrate'], a*sortedDf['pro-matches-winrate']+b)   
    # plt.show()
# plt.show()
# plotAgeAndWinrate()

def plotNationalityAndWinRate():
    nW = cleanDf[['nationality','pro-matches-winrate']]
    noDoubles = nW[nW['nationality'].str.contains('&') == False ]
    countOfPlayersInGroup = noDoubles.groupby(['nationality']).count()
    count = countOfPlayersInGroup.rename(columns={'pro-matches-winrate' : 'Number of Players in Nationality Group'})

    groupedByNationality = noDoubles.groupby(['nationality']).mean()
    print(groupedByNationality)
    ax = sns.scatterplot(x = groupedByNationality['pro-matches-winrate'], y=groupedByNationality.index, hue= count['Number of Players in Nationality Group'], size = count['Number of Players in Nationality Group'] )
    ax.set(
        xlabel = 'Mean Win Rate Within Nationality Group',
        ylabel = 'Nationality Group',
        title = 'Correlation Between Nationality and Win Rate'
    )
    ax.set_ylim(ymin=0, ymax=68)
    plt.tick_params(axis='y', labelsize='7', rotation = 0)
    plt.show()

plotNationalityAndWinRate()