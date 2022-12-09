#This program finds the answers to 2 of our questions by graphing them

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
def plotDiversityCount():
    rowID = 0
    diversityCount = []

    #iterate through each row to find every link per node
    while rowID<1021: #cleanDf has 1021 rows which is why i use that number
        nodeLinks =links.loc[links['Source'] == rowID] #gets node's edges in edge list
        targetNodes = nodeLinks['Target'] #these are the nodes that have a link with our current node (rowID)
        numberOfTargets = len(targetNodes) 

        targetRowID = 0
        linkAttributes = []
        uniqueLinkAttributesCount = 0

        #for each of the node's links, we get their attributes
        while targetRowID<numberOfTargets:
            targetAttributes = cleanDf.iloc[targetRowID] #get the target attributes
            targetAge = targetAttributes['age'] #get the age
            targetNat = targetAttributes['nationality'] #get nationality 
            #add attributes to our link attributes array
            linkAttributes.append(targetAge) 
            linkAttributes.append(targetNat)
            uniqueLinkAttributes = set(linkAttributes) # set only keeps unique attributes 
            uniqueLinkAttributesCount = len(uniqueLinkAttributes) #gets the number of unique attributes (this is our diversitycount/ player)
            targetRowID+=1
        
        diversityCount.append(uniqueLinkAttributesCount) #put number of unique attributes into our diversity count array
    
        rowID+=1


    i = 0
    dictLength = len(diversityCount)
    #calc avg winrate for each diversity count 
    uniqueDiversityCounts = set(diversityCount)
    diversityWinrate = {}

    #create a new dictionaty with winrate and diversity count
    while i<dictLength:
        diversityWinrate[i]={
                        'winrate': cleanDf.iloc[i]['pro-matches-winrate'], 
                        'diversityCount': diversityCount[i],
                        }
        i+=1
    diversityDf = pd.DataFrame.from_dict(diversityWinrate,orient='index') #create the dataframe from our dictionary
    i=0
    uniqueDiversityCountsSORTED = sorted(uniqueDiversityCounts) #sort by diversity count
    
    newdf = diversityDf.groupby(['diversityCount']).mean() #winrates in the diversity count group are averaged to get a single value
    counts = diversityDf.groupby(['diversityCount']).count()
    count = counts.rename(columns={'winrate' : 'Number of Players With Same Diversity Count'})


    ax = sns.scatterplot(x=newdf['winrate'],y=uniqueDiversityCountsSORTED, size=count['Number of Players With Same Diversity Count'])
    ax.set(
            xlabel = 'Mean Win Rate Among Players With Same Diversity Count',
            ylabel = 'Diversity Count',
            title = 'Correlation Between Playing Against A Diverse Number of Oppenents and Win Rate'
        )

    plt.show()



# How does a player's age & nationality affect their win rate?
def plotAgeAndWinrate():
    newdf = cleanDf[['age','pro-matches-winrate']]
    noRanges = newdf[cleanDf['age'].str.contains('-') == False ] #remove data that contains age range instead of single number
    countOfPlayersInAgeRange = noRanges.groupby(['age']).count() #get the size of the group
    count = countOfPlayersInAgeRange.rename(columns={'pro-matches-winrate' : 'Number of Players In Age Group'}) #rename column
    sortedCount = count.sort_index(ascending=True)
    avgWinratePerAge = noRanges.groupby(['age']).mean()
    
    sortedDf = avgWinratePerAge.sort_values(by=['age'],ascending=True) #sort values by age
    sortedAges = sorted(set(noRanges['age'])) #remove duplicates using set() and sort

    ax = sns.scatterplot(y = sortedDf['pro-matches-winrate'], x=sortedAges, size = sortedCount['Number of Players In Age Group'] )
    ax.set(
        xlabel = 'Mean Win Rate Within Age Group',
        ylabel = 'Age Group',
        title = 'Correlation Between Age and Win Rate'
    )
    plt.show()
 


def plotNationalityAndWinRate():
    nW = cleanDf[['nationality','pro-matches-winrate']]
    noDoubles = nW[nW['nationality'].str.contains('&') == False ] #some players had 2 nationalities e.g: canada & sweden. We removed these 
    countOfPlayersInGroup = noDoubles.sort_values(by=['pro-matches-winrate'],ascending=True).groupby(['nationality']).count() #get the size of the group
    count = countOfPlayersInGroup.rename(columns={'pro-matches-winrate' : 'Group Size'})

    groupedByNationality = noDoubles.groupby(['nationality']).mean()
    merged = groupedByNationality.merge(count, left_index=True, right_index=True, how='inner') #merge count with other df so we can plot it
    sortedDf = merged.sort_values(by=['pro-matches-winrate'],ascending=True) # sort values by win rate
    
    #scatterplot to show sizes
    ax = sns.scatterplot(x = sortedDf['pro-matches-winrate'], y=sortedDf.index, size=sortedDf['Group Size'], hue =sortedDf['Group Size'] )
    ax.set(
        xlabel = 'Mean Win Rate Within Nationality Group',
        ylabel = 'Nationality Group',
        title = 'Nationality and Win Rate'
    )
    ax.set_ylim(ymin=0, ymax=68)
    plt.tick_params(axis='y', labelsize='7', rotation = 0)
    plt.show()

    #bar graph
    bx = sns.barplot(x = sortedDf['pro-matches-winrate'], y=sortedDf.index, width=0.5)
    bx.set(
        xlabel = 'Mean Win Rate Within Nationality Group',
        ylabel = 'Nationality Group',
        title = 'Nationality and Win Rate'
    ) 
    bx.set_ylim(ymin=0, ymax=68)
    plt.tick_params(axis='y', labelsize='7', rotation = 0)
    plt.show()


plotNationalityAndWinRate()
plotAgeAndWinrate()
plotDiversityCount()