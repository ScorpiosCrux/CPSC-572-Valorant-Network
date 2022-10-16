import time

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

chromeDriverPath = "/Users/mar/Documents/SCHOOL/FALL2022/CPSC572/project/CPSC-572-Valorant-Network/chromedriver"

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
        


def getTeamInfo(team_url):
    while(True):
        break

def getPageContent(url,pathToContent):
    wait = WebDriverWait(driver, 1)
    extractedData = ''
    try:
        res = wait.until(EC.presence_of_element_located((By.XPATH, pathToContent)))
        extractedData = res.text
    except TimeoutException as e:
        print("\n Unable to locate page element. :( \n")
    return extractedData

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
    #Nested dictionary to hold data 
    # tournaments = {
    #     'tournament': {
    #         'name': '',
    #         'participants': [],
    #         'matches': [{
    #             'team1': {
    #                 'name': '',
    #                 'members': []
    #             },
    #             'team2':{
    #                 'name': '',
    #                 'members': []
    #             },
    #             'winner': ''
    #         }]
    #     }
    # }

    for url in page_urls:
        tournaments = {**tournaments,**getTournamentsAlgo(url,full_xpath)}
        # tournament_name = getTournamentsAlgo(url,full_xpath)[0]
        # tournament_info = getTournamentsAlgo(url,full_xpath)[1]
        # tournaments [tournament_name] = tournament_info
    return tournaments
    #should return a total of 254 turnaments 

def getTournamentsAlgo(page_url,full_xpath):
    # Function vars
    tournaments = {}
    tournament_name = ''                                                                                                                                            
    tournament_info = {}
    tournament_iteration = 2 

    #because the pages are structured differently, we must do an if statement :(
    if page_url == 'https://liquipedia.net/valorant/C-Tier_Tournaments':
        year_iteration = 4 
    else:
        year_iteration = 3                  #year:  4 = 2022, 5 = 2021  (for s-tier only)                                                                    
    
    getURL(page_url)                                                    # Uses the driver to open the URL
    formatted_xpath = full_xpath.format(year=year_iteration, tournament=tournament_iteration)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, formatted_xpath)))

    while (True):
        while(True):
            try:
                formatted_xpath = full_xpath.format(year=year_iteration, tournament=tournament_iteration)
                res = driver.find_element("xpath", formatted_xpath)
                tournament_name = res.get_attribute('text')
                tournament_link = res.get_attribute('href')
                tournament_info['participants'] = getTournamentParticipants(tournament_link)
                tournaments[tournament_name] = tournament_info
                
                
            except Exception as e:
                print(e.args[0])
                break
            tournament_iteration += 1

        tournament_iteration = 2                                                                                            # Reset Team Index
        year_iteration += 1

        if (year_iteration == 6 ):
            break

    return tournaments
    # return tournament_name , tournament_info


#creates an array that contains the names of each team in the tournament 
def getTournamentParticipants(tournament_link):
    xpath_participants = '/html/body/div[3]/main/div/div[3]/div[3]/div/div[10]/div[{row}]/div/div[{column}]/div/div/center/a'
                                              
    # tournament_link = 'https://liquipedia.net/valorant/VCT/2022/Champions'
    participants =  []
    participant = ''
    row_iteration = 1
    column_iteration = 1

    getURL(tournament_link)                                                    # Uses the driver to open the URL
    formatted_xpath = xpath_participants.format(row=row_iteration, column=column_iteration)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, formatted_xpath)))

    while (True):
        while(True):
            try:
                formatted_xpath = xpath_participants.format(row=row_iteration, column=column_iteration)
                res = driver.find_element("xpath", formatted_xpath)
                participant= res.get_attribute('text')
                participants.append(participant)    
            except Exception as e:
                print(e.args[0])
                break
            column_iteration += 1

        column_iteration = 1                                                                                            # Reset Team Index
        row_iteration += 1

        if (row_iteration >= 10 ):
            break

    return participants

def main():
    getTournaments()
    # getTournamentParticipants()
    # team_names, team_links = getTeams()
    # getTournaments()
    # Wait 3 seconds before deleting
    time.sleep(3)
    print("Done")

if __name__ == "__main__":
    main()
