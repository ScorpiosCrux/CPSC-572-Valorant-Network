import json
import pickle
import time


# Dumps a list in a file
def serializeList(file_name, list):
    with open(file_name, 'wb') as fp:
        pickle.dump(list, fp)

def readList(file_name):
    with open (file_name, 'rb') as fp:
        itemlist = pickle.load(fp)
    return itemlist

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

    serializeList("all_player_data", all_data)
    
    print("Finished Combining Data!")
    

def generateNodes(all_data):
    nodes = []
    id = 0
    for username, data in all_data.items():
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


        node = {
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
        nodes.append(node)
        id += 1

    return nodes

def exportJSON(file_name, nodes):
    with open(file_name, 'w') as fout:
        json.dump(nodes , fout, indent=4)

def importJSON(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)


def main():
    all_data = readList("all_player_data")
    nodes = generateNodes(all_data)
    exportJSON("nodes.json", nodes)
    
    print("Done")

if __name__ == "__main__":
    main()
