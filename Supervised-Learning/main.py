import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import pickle

# Reads the JSON file
def readJSON(file_name):
    with open(file_name, 'r') as myfile:
        data=myfile.read()
        return json.loads(data)

def createCSV(dataframe, filename):
    dataframe.to_csv(filename)


def removeRows(df, condition):
    return df[condition]

def main():
    data = readJSON("Main/nodes.json")

    df = pd.DataFrame(data)
    createCSV(df, 'Main/data.csv')
    print(df)

    df = df.rename({'pro-matches': 'matches', 'pro-matches-won': 'wins', 'pro-matches-lost': 'losses', 'pro-matches-winrate': 'winrate'}, axis=1)

    #Removes rows where age is empty
    df = df[df.age != '']
    df = df[df.age.str.contains('-') == False]
    df = df[df.winrate != '']
    print(df)


    #Convert string age to int
    print(df.dtypes)
    df = df.astype({'age': "int"})
    df = df.astype({'winrate': "float"})
    print(df.dtypes)
    
    createCSV(df, 'Main/data-cleaned.csv')

    sns.set(rc={"figure.figsize":(15, 8.5)}) 

    plot_order = df.sort_values("age")
    dis_plot = sns.histplot(data=plot_order, x="age")
    dis_plot.figure.savefig("Main/plot1.jpg") 
    plt.show()


    plot_order = df.sort_values("nationality")
    bar_plt = sns.barplot(data=plot_order, x=df.nationality.value_counts().index, y=df.nationality.value_counts(), order=df.nationality.value_counts()[:10].index)
    bar_plt.set(xlabel='nationality', ylabel='Count')
    bar_plt.figure.savefig("Main/plot2.jpg") 
    plt.show()


    scatter_plt = sns.scatterplot(data=df, x="matches", y="winrate")
    scatter_plt.figure.savefig("Main/plot3.jpg") 
    plt.show()

    print("Done")




if __name__ == "__main__":
    main()

