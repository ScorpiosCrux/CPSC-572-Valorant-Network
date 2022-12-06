#Credit to course notes for starter code - mainly from networkx-W3L5
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns

# change defaults to be less ugly
# Code for this section is from networkx-W3L5
mpl.rc('xtick', labelsize=14, color="#222222") 
mpl.rc('ytick', labelsize=14, color="#222222") 
mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
mpl.rc('font', size=16)
mpl.rc('xtick.major', size=6, width=1)
mpl.rc('xtick.minor', size=3, width=1)
mpl.rc('ytick.major', size=6, width=1)
mpl.rc('ytick.minor', size=3, width=1)
mpl.rc('axes', linewidth=1, edgecolor="#222222", labelcolor="#222222")
mpl.rc('text', usetex=False, color="#222222")

# Calculating degree distribution
# Code for this section is from networkx-W3L5
def deg_dist(degrees, kmin, kmax):
    # Get 10 logarithmically spaced bins between kmin and kmax
    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=10)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)

    fig = plt.figure(figsize=(6,4))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.loglog(x, density, marker='o', linestyle='none')
    # plt.plot(YBL)
    # plt.plot(x,density, marker='o', linestyle='none')
    plt.xlabel(r"degree $k$", fontsize=16)
    plt.ylabel(r"$P(k)$", fontsize=16)

    # remove right and top boundaries because they're ugly
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # Show the plot
    plt.show()

#Calculates average shortest path for each of the components
def shortest_path(G):
    print()
    print("Average Shortest Path Length for each Component:")
    
    #https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.average_shortest_path_length.html
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        averageSPL = nx.average_shortest_path_length(C, weight = True)
        print(averageSPL)

#Calculates average clustering coefficient for each of the components
def clustering_coefficient(G):
    print()
    print("Average Clustering Coefficient for each Component:")

    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        averageCustering = (nx.average_clustering(C, weight = True))
        print(averageCustering)


#Calculates the degree centrality and graphs it in relation to win rate
def calc_centrality(G):
    # loading in the nodes with attributes
    data = pd.read_csv("out.csv")
    df = pd.DataFrame(data)

    # getting rid of irrelevant columns
    df = df.drop(columns=["username", "age", "status", "nationality", "pro-matches", "pro-matches-won", "pro-matches-lost", "winnings"])

    # calculating the centrality
    degree_cent = nx.degree_centrality(G)

    # adding a column for degree centrality and filling it with "NA"
    df["degree centrality"] = "NA"

    # adding the degree centralities to the proper players 
    for key in degree_cent:
        df.loc[df[df["id"] == key].index,"degree centrality"]=degree_cent.get(key)
    
    #dropping rows without a degree centrality 
    df = df.drop(df[df["degree centrality"] == "NA"].index)

    #dropping players who have not participated in a tournament
    df = df.drop(df[df["tournaments"] <= 0].index)

    # getting rid of irrelevant columns
    df = df.drop(columns=["id", "tournaments"])

    # rounding the winrate to two decimal places so they can be effectively grouped and averaged
    df["pro-matches-winrate"] = df["pro-matches-winrate"].round(2)
    groupedByWinrate = df.groupby(['pro-matches-winrate']).mean()

    #plotting the correlation between degree centrality and win rate
    ax = sns.scatterplot(x=groupedByWinrate['degree centrality'], y = groupedByWinrate.index)
    ax.set(
        xlabel = 'Degree Centrality',
        ylabel = 'Win Rate',
        title = 'Correlation Between Degree Centrality and Win Rate'
    )

    #find line of best fit
    x = groupedByWinrate['degree centrality']
    y = groupedByWinrate.index
    a, b = np.polyfit(x, y, 1)
    #add line of best fit to plot
    plt.plot(x, a*x+b, color= "red")

    plt.show()

def main():
    links = open("links.csv", "r")
    next(links, None)  # skip the first line in the input file

    #reading in edge list
    G = nx.read_weighted_edgelist(links, delimiter=',', create_using=nx.Graph(), nodetype=int)

    #calculating the # nodes, # links, average degree, minimum degree, and maximum degree
    # Code for this section is from networkx-W3L5
    N = len(G)
    L = G.size()
    degrees = [G.degree(node) for node in G]
    kmin = min(degrees)
    kmax = max(degrees)

    print("Number of nodes: ", N)
    print("Number of edges: ", L)
    print()
    print("Average degree: ", 2*L/N)
    print("Average degree (alternate calculation)", np.mean(degrees))
    print()
    print("Minimum degree: ", kmin)
    print("Maximum degree: ", kmax)
    
    # deg_dist(degrees, kmin, kmax)
    
    print()
    print("Number of Components: ", nx.number_connected_components(G))
    
    shortest_path(G)
    clustering_coefficient(G)
    calc_centrality(G)

main()
