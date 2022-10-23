import time
import pickle
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait



chrome_options = Options()

# IMPORTANT: Uncomment this if the page is not loading because your window is behind 
# chrome_options.add_argument("--headless")

chromeDriverPath = "./chromedriver"

service = Service(executable_path=chromeDriverPath)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_window_position(0, 0)



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
        


def getTeamInfo(team_url):
    while(True):
        break


def getTournaments():

    page_urls = [
                'https://liquipedia.net/valorant/S-Tier_Tournaments',
                'https://liquipedia.net/valorant/A-Tier_Tournaments',
                'https://liquipedia.net/valorant/B-Tier_Tournaments',
                'https://liquipedia.net/valorant/C-Tier_Tournaments',
                ]

    #year: 4 = 2022, 5 = 2021
    #tournament: row # within div.. R1 = 2, R2 = 3, R3 = 4 and so on.
    full_xpath = '/html/body/div[3]/main/div/div[3]/div[3]/div/div[{year}]/div/div[{tournament}]/div[1]/b/a'
    tournaments={}
    tournament_names=[]
    tournament_links=[]
    
    result = ()
    for url in page_urls:
        names, links = getTournamentsAlgo(page_url=url, full_xpath=full_xpath)
        tournament_names=tournament_names + names
        tournament_links.extend(links)
        
    return tournament_names, tournament_links
    #should return a total of 252 turnaments 

def getTournamentsAlgo(page_url,full_xpath):
    # Function vars
    tournament_links = []
    tournament_names = []
    tournament_info = {}
    tournament_iteration = 2 
    getURL(page_url)
    wait = WebDriverWait(driver, 1)


    try:
        
        res = driver.find_elements(By.CLASS_NAME, 'divCell.Tournament.Header')
        for item in res:
            tournament_name = item.find_element(By.XPATH, './b/a').text
            tournament_link = item.find_element(By.XPATH, './b/a').get_attribute('href')
            
            tournament_links.append(tournament_link)
            tournament_names.append(tournament_name)
            
    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    

   
    return tournament_names,tournament_links
    # return tournament_name , tournament_info


#creates an array that contains the names of each team in the tournament 
def getTournamentParticipants(tournament_link):
    driver.get(tournament_link)                                        
    participants =  []

    try:
        res = driver.find_elements(By.CLASS_NAME, 'teamcard')
        for item in res:
            name=item.find_element(By.XPATH, './center/a').text
            participants.append(name)
    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    return participants

def getTournamentMatches(tournament_link):
    driver.get(tournament_link)                                        
    matches =  []
    teams = set()
    team_members = {}

    try:
        res = driver.find_elements(By.CLASS_NAME, 'brkts-match')
        for item in res:
            t1 = item.find_element(By.CLASS_NAME, 'name.hidden-xs').text
            t2 = item.find_element(By.XPATH, './div/following-sibling::div/div/div/span/following-sibling::span').text
            winner = item.find_element(By.CLASS_NAME,'brkts-opponent-win').find_element(By.CLASS_NAME,'name.hidden-xs').text
            matches.append({
                t1: '', 
                t2: '',
                'winner': winner
                })
            teams.add(t1)
            teams.add(t2)

        wait = WebDriverWait(driver, 1)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Show Players"]')))
        res = driver.find_element(By.XPATH, '//button[text()="Show Players"]')
        driver.execute_script("arguments[0].click();", res)

        team_info={}
        for team in teams:
            url = tournament_link
            members = getTournamentTeamMembers(url, team)
            team_members[team]=members

        
        for match in matches:
            for team in team_members:
                if team in match:
                    match[team]=team_members[team]

    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    return matches

def getTournamentTeamMembers(url,team):
    getURL(url)
    members = []
    
    try:
        res = driver.find_elements(By.XPATH, '//*[@title="'+team+'"]/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')
        
        if res==[]:
            res = driver.find_elements(By.XPATH, '//*[@title="'+team+'"]/parent::a/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')

        for item in res:
            # member = item.find_element(By.XPATH, './td/a').text
            elements = item.find_elements(By.XPATH, './td/a')
            for name in elements:
                member = name.get_attribute('title')
                member = member.replace(' (page does not exist)','')
                members.append(member)
     

    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    return members

# Dumps a list in a file
def serializeList(file_name, list):
    with open(file_name, 'w') as convert_file:
     convert_file.write(json.dumps(list))
    # with open(file_name, 'wb') as fp:
    #     pickle.dump(str(list), fp)

def main():

    tournamentsWithInfo = {}
    
    tournaments = getTournaments()
    tournament_names=tournaments[0]
    tournament_links=tournaments[1]
    index = 0
    
    for name in tournament_names:
        tournamentsWithInfo[name] = {}
        participants = getTournamentParticipants(tournament_links[index])
        matches = getTournamentMatches(tournament_links[index])
        tournamentsWithInfo[name] = {'participants':participants, 'matches':matches}
        serializeList('tournament_info_NEW',tournamentsWithInfo)

        index+=1

    serializeList('tournament_info',tournamentsWithInfo)




   
    time.sleep(3)
    print("Done")

if __name__ == "__main__":
    main()
