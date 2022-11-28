import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import json

# change defaults to be less ugly
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

def main():
    f = open('nodes_all.json')
    nodes = json.load(f)
    f.close()

    G = nx.Graph()
    # # adding nodes from dictionary
    # G.add_nodes_from(nodes.keys())

    # #adding attributes
    # for key,playerD in G.nodes.items():
    #     playerD["id"]=nodes[key]["id"]
    #     playerD["username"]=nodes[key]["username"]
    #     playerD["age"]=nodes[key]["age"]
    #     playerD["status"]=nodes[key]["status"]
    #     playerD["nationality"]=nodes[key]["nationality"]
    #     playerD["pro-matches"]=nodes[key]["pro-matches"]
    #     playerD["pro-matches-won"]=nodes[key]["pro-matches-won"]
    #     playerD["pro-matches-lost"]=nodes[key]["pro-matches-lost"]
    #     playerD["pro-matches-winrate"]=nodes[key]["pro-matches-winrate"]
    #     playerD["tournaments"]=nodes[key]["tournaments"]
    #     playerD["winnings"]=nodes[key]["winnings"]

    # print("ID: ", G.nodes["10x"]["id"]," pro matches: ",G.nodes["10x"]["pro-matches"])
    links = open('links.csv', "r")
    next(links, None)  # skip the first line in the input file

    #reading in edge list
    G = nx.parse_edgelist(links, 
                        delimiter=',', 
                        create_using=nx.Graph(),
                        nodetype=int)
    
    # for n1, n2, data in G.edges(data=True):
    #     print("{0} <----> {1}: {2}".format(n1, n2, data))

    # all nodes (returns a dictionary with node : degree pairs for all nodes)
    # print(G.degree())

    # using the force-based or "spring" layout algorithm
    # fig = plt.figure(figsize=(8,8))
    # nx.draw_networkx(G)
    # nx.draw_spring(G, node_size=40)
    # plt.show()

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

    # # Get 10 logarithmically spaced bins between kmin and kmax
    # bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=10)

    # # histogram the data into these bins
    # density, _ = np.histogram(degrees, bins=bin_edges, density=True)

    # fig = plt.figure(figsize=(6,4))

    # # "x" should be midpoint (IN LOG SPACE) of each bin
    # log_be = np.log10(bin_edges)
    # x = 10**((log_be[1:] + log_be[:-1])/2)

    # plt.loglog(x, density, marker='o', linestyle='none')
    # plt.xlabel(r"degree $k$", fontsize=16)
    # plt.ylabel(r"$P(k)$", fontsize=16)

    # # remove right and top boundaries because they're ugly
    # ax = plt.gca()
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # ax.yaxis.set_ticks_position('left')
    # ax.xaxis.set_ticks_position('bottom')
    
    # # Show the plot
    # plt.show()

    # Get 20 logarithmically spaced bins between kmin and kmax
    bin_edges = np.linspace(kmin, kmax, num=10)

    # histogram the data into these bins
    density, _ = np.histogram(degrees, bins=bin_edges, density=True)

    fig = plt.figure(figsize=(6,4))

    # "x" should be midpoint (IN LOG SPACE) of each bin
    log_be = np.log10(bin_edges)
    x = 10**((log_be[1:] + log_be[:-1])/2)

    plt.plot(x, density, marker='o', linestyle='none')
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


    print("Done")
    
main()
