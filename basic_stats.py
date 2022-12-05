#Credit to course notes for starter code - mainly from networkx-W3L5
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

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


#Calculates various types of centrality and prints them
def calc_centrality(G):
    data = pd.read_csv('out.csv')
    df = pd.DataFrame(data)

    print()
    print("Centrality Calculations:")

    degree_cent = nx.degree_centrality(G)
    print("Degree Centrality: ", degree_cent)
    betweeness_cent = nx.betweenness_centrality(G)
    print("Betweeness Centrality: ", betweeness_cent)
    closeness_cent = nx.closeness_centrality(G)
    print("Closeness Centrality: ", closeness_cent)

def main():
    links = open('links.csv', "r")
    next(links, None)  # skip the first line in the input file

    #reading in edge list
    G = nx.read_weighted_edgelist(links, delimiter=',', create_using=nx.Graph(), nodetype=int)

    #calculating the # nodes, # links, average degree, minimum degree, and maximum degree
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
    
    deg_dist(degrees, kmin, kmax)
    
    print()
    print("Number of Components: ", nx.number_connected_components(G))
    
    # shortest_path(G)
    # clustering_coefficient(G)
    calc_centrality(G)

main()
