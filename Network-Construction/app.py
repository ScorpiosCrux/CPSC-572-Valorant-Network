
# Imports
import json
import pickle
import time
import pandas as pd

# Dumps a list in a file using Pickle
def serializeList(file_name, list):
    with open(file_name, 'wb') as fp:
        pickle.dump(list, fp)

# Reads a list using pickle
def readList(file_name):
    with open (file_name, 'rb') as fp:
        itemlist = pickle.load(fp)
    return itemlist

# Exports nodes as JSON
def exportJSON(file_name, nodes):
    with open(file_name, 'w') as fout:
        json.dump(nodes , fout, indent=4)

# Import JSON file and return data
def importJSON(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data

# Creates a CSV file with header as "Source, Target"
def writeFile(file_name, data):
    with open(file_name, "w") as f:
        f.write("Source,Target\n")
        for item in data:
            f.write(item + '\n')

# Uses Pandas to create a CSV file.
def pandaCSV(file_name, data):
    pf = pd.DataFrame(data).T
    pf.to_csv(file_name, index=False)

# Combines all the player data into a single file.
def combinePlayerData():
    file_names = [
                    "all_player_data0-200",
                    "all_player_data199-300",
                    "all_player_data299-400",
                    "all_player_data399-500",
                    "all_player_data499-600",
                    "all_player_data599-700",
                    "all_player_data699-800",
                    "all_player_data799-900",
                    "all_player_data899-1000",
                    "all_player_data1000-1100",
                    "all_player_data1100-1200",
                    "all_player_data1199-1300",
                    "all_player_data1299-1400",
                    "all_player_data1400-1500",
                    "all_player_data1499-1600",
                    "all_player_data1599-1700",
                    "all_player_data1699-1800",
                    "all_player_data1799-1900",
                    "all_player_data1899-2000",
                    "all_player_data2000-2031",
                ]

    all_data = {}
    for file_name in file_names:
        data = readList(file_name)
        all_data.update(data)

    # Exports as a single file.
    serializeList("all_player_data", all_data)
    
    print("Finished Combining Data!")

# Creates the nodes by putting all the data into a single dictionary
def generateNodes(all_data):
    nodes = {}
    # nodes = []
    id = 0
    for username, data in all_data.items():
        username = username.lower()
        tournaments = set()
        total_games = len(data['matches'])
        games_won = 0
        for match in data["matches"]:
            if match['result'] == "won":
                games_won += 1
            tournaments.add(match['tournament'])
            

        if total_games != 0:
            win_rate = games_won/total_games
        else:
            win_rate = ""


        nodes[username] = {
            "id": id,
            "username": username,
            "age": data['age'],
            "status": data['status'],
            "nationality": data['nationality'],
            "pro-matches": len(data['matches']),
            "pro-matches-won": games_won,
            "pro-matches-lost": total_games - games_won,
            "pro-matches-winrate": win_rate,
            "tournaments": len(tournaments),
            "winnings": data['winnings']
        }
        #nodes.append(node)
        id += 1

    return id, nodes

# If we're unable to find the player in the nodes list,
# the data does not exist for that individual. We therefore add the player
# as a new node.
def getPlayerID(nodes, name, id):
    try:
        player = nodes[name]
        player_id = player["id"]
        return player_id, id
    except:
        print("Cannot find: " + name)
        nodes[name] = {
            "id": id,
            "username": name,
            "age": "",
            "status": "",
            "nationality": "",
            "pro-matches": -1,
            "pro-matches-won": -1,
            "pro-matches-lost": -1,
            "pro-matches-winrate": -1,
            "tournaments": -1,
            "winnings": ""
        }
        id += 1

        player = nodes[name]
        player_id = player["id"]
        return player_id, id
        


# Generates the links depending on who their teammates are.
def generateTeamLinks(nodes, id):
    tournament_data = importJSON("tournament_info_2.0")
    links = []

    # For each tournament, get the matches and the team members.
    # With the team members, draw a complete with that.
    for tournament, data in tournament_data.items():
        matches = data['matches']
        if (len(matches) != 0):
            for match in matches:
                for key, team in match.items():
                    if (key == 'winner'):
                        continue

                    # Draws a complete graph on the nodes
                    increment = 0
                    for i in range(increment, len(team)):
                        for j in range(increment, len(team)):

                            player_1 = team[i].lower()
                            player_2 = team[j].lower()

                            if (player_1 == player_2):
                                continue
                            
                            player_1_id, id = getPlayerID(nodes=nodes, name=player_1, id=id)
                            player_2_id, id = getPlayerID(nodes=nodes, name=player_2, id=id)

                            link = "{},{}".format(player_1_id, player_2_id)
                            links.append(link)
                        increment += 1
    return links

# Generates the links depending on who they've played with. 
def generateMatchLinks(nodes, id):
    tournament_data = importJSON("Data/Main-Data/tournament_info_2.0")
    links = []

    # Error tracking.
    error_num = 0
    success_num = 0

    # For each tournament get all the matches.
    for tournament, data in tournament_data.items():
        matches = data['matches']
        if (len(matches) != 0):
            for match in matches:
                team_a = None
                team_b = None

                # Parse the data to get the two teams
                for key, team in match.items():
                    if (key == 'winner'):   # Winner is set as a key at the same level as the teams.
                        continue
                    if (team_a == None):
                        team_a = team
                    else:
                        team_b = team

                # If the teams are empty then report error and move on.
                if (len(team_a) == 0 or len(team_b) == 0):
                    error_num += 1
                    print(str(error_num) + "Error!" + str(tournament))
                    continue

                # For each player in team_a, link them with all players on team_b
                # Creates a csv string. E.g. 2302, 1202
                for player_a in team_a:
                    for player_b in team_b:

                        player_a = player_a.lower()
                        player_b = player_b.lower()
                        
                        player_a_id, id = getPlayerID(nodes=nodes, name=player_a, id=id)
                        player_b_id, id = getPlayerID(nodes=nodes, name=player_b, id=id)

                        link = "{},{}".format(player_a_id, player_b_id)
                        links.append(link)

                # For error reporting
                success_num += 1

    return links

# Generate weighted links as Gephi and Network X have a hard time parsing our unweighted nodes list.
def generatedWeightedLinks(links):
    weights = {}
    for link in links:
        if (link in weights):
            weights[link] += 1
        else:
            weights[link] = 1
        print("Done")
    
    #https://stackoverflow.com/questions/4183506/python-list-sort-in-descending-order
    sorted_weights = {k: v for k, v in sorted(weights.items(), key=lambda item: item[1], reverse=True)}

    # Write the file to Data/Main-Data/links.csv
    with open("Data/Main-Data/links.csv", "w") as f:
        f.write("Source,Target,Weight\n")
        for item in sorted_weights:
            f.write(item + "," + str(weights[item]) + '\n')


def main():
    # Read all the player data
    all_data = readList("Webscraping/player-data/all_player_data")

    # Passes the player data to the generate nodes function
    id, nodes = generateNodes(all_data)

    # We generate the links on tournament data, if there are players we've never heard of,
    # we add those nodes to the previous nodes
    links = generateMatchLinks(nodes, id)
    
    # Generates the weighted links
    generatedWeightedLinks(links)
    

    # Exports the all the data
    # exportJSON("nodes_all.json", nodes)
    # pandaCSV("nodes_all.csv", nodes)
    # writeFile("links.csv", data)

    print("Done")

if __name__ == "__main__":
    main()
