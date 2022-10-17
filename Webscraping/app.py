
import json
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()

# IMPORTANT: Uncomment this if the page is not loading because your window is behind 
#chrome_options.add_argument("--headless")

#chromeDriverPath = "C:\\Users\\jasmi\\Desktop\\CPSC572\\CPSC-572-Valorant-Network\\Webscraping\\chromedriver.exe"
chromeDriverPath = './Webscraping/chromedriver'

service = Service(executable_path=chromeDriverPath)
driver = webdriver.Chrome(service=service, options=chrome_options)


#Get the URL, you can add exception handling here or even assertions
def getURL(url):
    driver.get(url)


# Example Code
# Highly documented for understanding
# This function gets all the teams names and team links for each region
def getTeams():
    # Hardcoded vars
    page_urls = [
            "https://liquipedia.net/valorant/index.php?title=Category:Teams",
            "https://liquipedia.net/valorant/index.php?title=Category:Teams&pagefrom=Kafalar+Esports#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Teams&pagefrom=Team+nxl#mw-pages"
                ]
    full_xpath = "/html/body/div[3]/main/div/div[3]/div[3]/div[2]/div[2]/div/div/div[{letter}]/ul/li[{team}]/a"             # This is the path to where you want to find the location. Can be found using inspect element and then copying the xpath. {} denotes where we want to add values
    
    team_names = []
    team_links = []
    for page_url in page_urls:
        names, links = getTeamsAlgo(page_url=page_url, full_xpath=full_xpath)
        team_names.extend(names)
        team_links.extend(links)
        
    return team_names, team_links

# Algorithm for getting team information
def getTeamsAlgo(page_url, full_xpath):
    # Function vars
    team_names = []                                                                                         # Storing the team names in a list
    team_links = []                                                                                         # Storing the links in a list
    letter_iteration = 1                                                                                              # Starts at the first letter category. Used by while loop
    team_iteration = 1                                                                                                # Starts at the first team inside the letter category.

    getURL(page_url)                                                                                        # Uses the driver to open the URL
    formatted_xpath = full_xpath.format(letter=letter_iteration, team=team_iteration)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, formatted_xpath)))

    while (True):
        while(True):
            try:
                formatted_xpath = full_xpath.format(letter=letter_iteration, team=team_iteration)
                res = driver.find_element("xpath", formatted_xpath)
                name = res.get_attribute('text')
                link = res.get_attribute('href')
                team_names.append(name)
                team_links.append(link)
            except Exception as e:
                print(e.args[0])
                break
            team_iteration += 1

        team_iteration = 1                                                                                            # Reset Team Index
        letter_iteration += 1

        if (letter_iteration == 36 ):
            break

    return team_names, team_links
        

# Dumps a list in a file
def serializeList(file_name, list):
    with open(file_name, 'wb') as fp:
        pickle.dump(list, fp)

def readList(file_name):
    with open (file_name, 'rb') as fp:
        itemlist = pickle.load(fp)
    return itemlist



def getTeamInfo(team_link):

    print("Working on: " + team_link)
    getURL(team_link)
    wait = WebDriverWait(driver, 1)


    data = {}

    # Team Name
    try:
        res = wait.until(EC.presence_of_element_located((By.XPATH, "//h1/span")))
        team_name = res.text
        data["team-name"] = team_name
    except TimeoutException as e:
        print("\n Unable to locate team_name! \n")

    # Country
    try:
        # Find element div tag with Location as text. Then get it's sibling which is a div
        res = driver.find_element(By.XPATH, '//div[text()="Location:"]/following-sibling::div')
        country = res.text.strip()
        data["country"] = country
    except NoSuchElementException:
        data["country"] = ""
        print("\n Unable to locate country! \n")

    # Region
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Region:"]/following-sibling::div')
        region = res.text.strip()
        data["region"] = region
    except NoSuchElementException:
        data["region"] = ""
        print("\n Unable to locate region! \n")
    
    # Winnings
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Approx. Total Winnings:"]/following-sibling::div')
        winnings = res.text.strip()
        data["winnings"] = winnings
    except NoSuchElementException:
        data["winnings"] = ""
        print("\n Unable to locate winnings! \n")

    # Status
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Disbanded"]/following-sibling::div')
        data["status"] = "disbanded"
    except NoSuchElementException:
        data["status"] = "active"


    # Click on show all button, need to execute script because button is not visible for click
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//h3/span[@id="Former"]//parent::h3//following-sibling::div/ul/li[@class="show-all"]/a[text()="Show All"]')))
        res = driver.find_element(By.XPATH, '//h3/span[@id="Former"]//parent::h3//following-sibling::div/ul/li[@class="show-all"]/a[text()="Show All"]')
        driver.execute_script("arguments[0].click();", res)
    except TimeoutException:
        print('No Former "Show All" button found! Skipping...')
    except NoSuchElementException:
        print("Cannot find Show All Button")

    try:
        data["players"] = []
        res = driver.find_elements(By.XPATH, '//tr[@class="Player"]')
        for item in res:
            id = item.find_element(By.XPATH, './td[@class="ID"]').text
            name = item.find_element(By.XPATH, './td[@class="Name"]').text
            data["players"].append({"username":id, "name":name})
    except NoSuchElementException:
        print("\n Unable to locate players! \n")


    return data

def getAllTeamInfo(all_team_links):
    all_team_data = {}
    for link in all_team_links:
        team_data = getTeamInfo(link)
        all_team_data[team_data["team-name"]] = team_data

    
    return all_team_data


#Get Players ---------------------------------------------------------------------------------------------------
def getPlayers():
    # Hardcoded vars
    page_urls = [
            "https://liquipedia.net/valorant/index.php?title=Category:Players",            
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Bigas#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Darrick#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Flax#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Jax#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Lawrence#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Mt1xo#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Poiz#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Shehab#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Tiraye#mw-pages",
            "https://liquipedia.net/valorant/index.php?title=Category:Players&pagefrom=Zeddy#mw-pages"
                ]

    # This is the path to where you want to find the location. Can be found using inspect element and then copying the xpath. {} denotes where we want to add values          
    full_xpath = "/html/body/div[3]/main/div/div[3]/div[3]/div[2]/div[2]/div/div/div[{letter}]/ul/li[{player}]/a"

    player_names = []
    player_links = []
    for page_url in page_urls:
        names, links = getPlayersAlgo(page_url=page_url, full_xpath=full_xpath)
        player_names.extend(names)
        player_links.extend(links)
        
    return player_names, player_links

# Algorithm for getting team information
def getPlayersAlgo(page_url, full_xpath):
    # Function vars
    player_names = []                                                                                     # Storing the player names in a list
    player_links = []                                                                                     # Storing the links in a list
    letter_iteration = 1                                                                                  # Starts at the first category. Used by while loop
    player_iteration = 1                                                                                  # Starts at the first player inside the category.

    getURL(page_url)                                                                                      # Uses the driver to open the URL
    formatted_xpath = full_xpath.format(letter=letter_iteration, player=player_iteration)
    WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, formatted_xpath)))

    while (True):
        while(True):
            try:
                formatted_xpath = full_xpath.format(letter=letter_iteration, player=player_iteration)
                res = driver.find_element("xpath", formatted_xpath)
                name = res.get_attribute('text')
                link = res.get_attribute('href')
                player_names.append(name)
                player_links.append(link)
            except Exception as e:
                print(e.args[0])
                break
            player_iteration += 1

        player_iteration = 1                                                                                            # Reset Team Index
        letter_iteration += 1

        if (letter_iteration == 36 ):
            break

    return player_names, player_links

def getPlayerInfo(player_link):

    print("Working on: " + player_link)
    getURL(player_link)
    wait = WebDriverWait(driver, 1)
    data = {}

    # Player Name
    try:
        res = wait.until(EC.presence_of_element_located((By.XPATH, "//h1/span")))
        player_name = res.text
        data["player-name"] = player_name
    except TimeoutException as e:
        print("\n Unable to locate player_name! \n")

    # Nationality
    try:
        # Find element div tag with Location as text. Then get it's sibling which is a div
        res = driver.find_element(By.XPATH, '//div[text()="Nationality:"]/following-sibling::div')
        nationality_full = res.text.strip()
        nationality = nationality_full.replace("\n"," &")
        data["nationality"] = nationality
    except NoSuchElementException:
        data["nationality"] = ""
        print("\n Unable to locate nationality! \n")

    # Age
    try:
        # Find element div tag with Location as text. Then get it's sibling which is a div
        res = driver.find_element(By.XPATH, '//div[text()="Born:"]/following-sibling::div')
        birth_info = res.text.strip()
        birth_info_shortened = birth_info.split("age ",1)[1]
        age = birth_info_shortened.replace(")","")
        data["age"] = age
    except IndexError:
        data["age"] = ""
        print("\n Unable to locate age! \n")    
    except NoSuchElementException:
        data["age"] = ""
        print("\n Unable to locate age! \n")

    # Status
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Status:"]/following-sibling::div')
        status = res.text.strip()
        data["status"] = status
    except NoSuchElementException:
        data["status"] = ""

    # Team
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Team:"]/following-sibling::div')
        region = res.text.strip()
        data["team"] = region
    except NoSuchElementException:
        data["team"] = ""
        print("\n Unable to locate team! \n")
    
    # Winnings
    try:
        res = driver.find_element(By.XPATH, '//div[text()="Approx. Total Winnings:"]/following-sibling::div')
        winnings = res.text.strip()
        data["winnings"] = winnings
    except NoSuchElementException:
        data["winnings"] = ""
        print("\n Unable to locate winnings! \n")


    # View player matches
    matches_link = player_link + "/Matches"
    getURL(matches_link)

    try:
        data["matches"] = []
        res = driver.find_elements(By.XPATH, '//table[@class="wikitable wikitable-striped sortable jquery-tablesorter"]/tbody/tr')
        for item in res:
            style = item.get_attribute('style').split("rgb",1)[1]
            if style == "(240, 255, 240);":
                result = "won"
            else:
                result = "lost"
            tournament_name = item.find_element(By.XPATH, './td[5]').text
            team_name = item.find_element(By.XPATH, './td[13]/span/span/a').get_attribute('title')
            data["matches"].append({"tournament":tournament_name,"result":result, "team":team_name})
    except NoSuchElementException:
        print("\n Unable to locate matches! \n")
    except IndexError:
        print("\n Unable to locate matches! \n")


    return data

def getAllPlayerInfo(all_player_links):
    
    all_player_data = {}

    for link in all_player_links:
        try:
            player_data = getPlayerInfo(link)
            all_player_data[player_data["player-name"]] = player_data
        except Exception as e:
            print('ERROR!')
   
    return all_player_data


def mineTeamData():
    team_names, team_links = getTeams()
    
    serializeList("team_links", team_links)
    team_links = readList("team_links")

    all_team_data = getAllTeamInfo(team_links)

    player_names, player_links = getPlayers()
    serializeList("player_links", player_links)

def minePlayerData():
    all_player_links = readList("player_links")
    start = 2000
    end = 2031
    load = all_player_links[start:end]

    all_player_data = getAllPlayerInfo(load)
    
    serializeList("all_player_data" + str(start) + "-" + str(end), all_player_data)





def main():



   

    
    print("Done")

if __name__ == "__main__":
    main()
