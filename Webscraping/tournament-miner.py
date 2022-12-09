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

chromeDriverPath = "../chromedriver"

service = Service(executable_path=chromeDriverPath)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_window_position(0, 0)


#Get the URL, you can add exception handling here or even assertions
def getURL(url):
    driver.get(url)


def getTournaments():

    #these are the pages where tournaments are listed 
    #pages are divided into S A B C tier tournaments 
    page_urls = [
                'https://liquipedia.net/valorant/S-Tier_Tournaments',
                'https://liquipedia.net/valorant/A-Tier_Tournaments',
                'https://liquipedia.net/valorant/B-Tier_Tournaments',
                'https://liquipedia.net/valorant/C-Tier_Tournaments',
                ]

    #by looking at the pages we must identify patters to form the requred xpath that gets us the information we need
    #identified pattern: year: 4 = 2022, 5 = 2021 etc
    #another pattern: tournament: row # within div.. R1 = 2, R2 = 3, R3 = 4 and so on.

    full_xpath = '/html/body/div[3]/main/div/div[3]/div[3]/div/div[{year}]/div/div[{tournament}]/div[1]/b/a'
    
    #we will get the name of the tournament and the link of the tournamnet page
    tournament_names=[]
    tournament_links=[]
    
    #to get all tournaments we must get all the tournaments in each page.
    for url in page_urls:
        names, links = getTournamentsAlgo(page_url=url, full_xpath=full_xpath)
        tournament_names=tournament_names + names
        tournament_links.extend(links)
        
    return tournament_names, tournament_links
    #should return a total of 252 turnaments 
    #returns tuple of names and page links

def getTournamentsAlgo(page_url,full_xpath):
    # Function vars
    tournament_links = []
    tournament_names = []
    tournament_info = {}
    tournament_iteration = 2 
    getURL(page_url)
    wait = WebDriverWait(driver, 1) #wait until page is loaded so we dont get error


    try:
        #we are getting the info by the HTML class name
        res = driver.find_elements(By.CLASS_NAME, 'divCell.Tournament.Header') #gets all elements in the page with that class name
        for item in res:
            #xpath goes into where we are currently and then we look at the HTML structure of the webpage
            tournament_name = item.find_element(By.XPATH, './b/a').text #the data we want is under a <b> tag and then an <a> tag and we get the text inside that container which is the tournament name
            tournament_link = item.find_element(By.XPATH, './b/a').get_attribute('href') #now we het the href inside the <a> tag which gives us the tournament link
            
            tournament_links.append(tournament_link) #append that info to our array
            tournament_names.append(tournament_name)
            
    except NoSuchElementException as e: #in case it can't find anything in the xpath
        print("\n Unable to locate page element. :( \n")


   
    return tournament_names,tournament_links
    # returns our arrays in a tuple


#creates an array that contains the names of each team in the tournament 
def getTournamentParticipants(tournament_link):
    driver.get(tournament_link)                                        
    participants =  []

    try:
        res = driver.find_elements(By.CLASS_NAME, 'teamcard') #gets all elements with teamcard as their class name
        for item in res:
            name=item.find_element(By.XPATH, './center/a').text #team name is under this xpath
            participants.append(name) #add that name to our tournament participants
    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    return participants

#now we get the actual match info! This is important because this is how we will link nodes together in out network
def getTournamentMatches(tournament_link): 
    driver.get(tournament_link)                                        
    matches =  []
    teams = set() #teams is a set so we don't get duplicates
    team_members = {}

    try:
        res = driver.find_elements(By.CLASS_NAME, 'brkts-match') #sometimes match info is under this class name
    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    #it is common for this website to have pages for the same stuff with slight differences in their HTML
    if res == []: #if res comes back as an empty array we must try different things 
        try:
            res = driver.find_elements(By.CLASS_NAME, 'bracket-game') #sometimes match info is under this other class name 
            for item in res:
                try:
                    t1 = item.find_element(By.CLASS_NAME,'bracket-team-top').get_attribute('data-highlightingkey') #get the first team that played in that match
                    t2 = item.find_element(By.CLASS_NAME,'bracket-team-bottom').get_attribute('data-highlightingkey') # get the 2nd team that played in that match
                    winner = item.find_element(By.XPATH,'./*[@style="font-weight:bold"]/div').get_attribute('data-highlightingkey') #get the winner team of the match
                    #put matches into a dictionary
                    matches.append({
                        t1: '', 
                        t2: '',
                        'winner': winner
                        })
                    teams.add(t1)
                    teams.add(t2)
                except NoSuchElementException as e:
                    print("\n Unable to locate page element in loop in case1. \n")
        except NoSuchElementException as e:
            print("\n Unable to locate page element in case1. \n")

    else: #if the first res didnt come back empty we can try the stuff below
        try:
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
        except NoSuchElementException as e:
            print("\n Unable to locate page element in case 2. \n")

    wait = WebDriverWait(driver, 1) #wait for the page to load first
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Show Players"]')))
    res = driver.find_element(By.XPATH, '//button[text()="Show Players"]')
    driver.execute_script("arguments[0].click();", res) #click the button that shows players so that we can get player info

    team_info={}
    for team in teams:
        url = tournament_link
        members = getTournamentTeamMembers(url, team)
        team_members[team]=members #we put our into into the dict


    for match in matches:
        for team in team_members:
            if team in match:
                match[team]=team_members[team] #put the info into the dict

    return matches
#we get the names of all players in each team 
def getTournamentTeamMembers(url,team):
    getURL(url)
    members = []
    
    #some tournament pages had different formats. We had to try to handle every case in order to get the data.
    #that is the reason for the if statements 
    try:
        res = driver.find_elements(By.XPATH, '//*[@title="'+team+'"]/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')
        
        if res==[]:
            res = driver.find_elements(By.XPATH, '//*[@title="'+team+'"]/parent::a/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')
        if res==[]:
            res = driver.find_elements(By.XPATH, '//*[text()="'+team+'"]/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')
        if res==[]:
            res = driver.find_elements(By.XPATH, '//*[@title="'+team+' (page does not exist)"]/parent::center/following-sibling::div[@class="teamcard-inner"]/table[@data-toggle-area-content="1"]/tbody/tr')
         
        for item in res:
            elements = item.find_elements(By.XPATH, './td/a')
            for name in elements:
                member = name.get_attribute('title')
                member = member.replace(' (page does not exist)','') #some players had (page does not exist) appended to their name so we remove that 
                members.append(member)
     

    except NoSuchElementException as e:
        print("\n Unable to locate page element. :( \n")

    return members

# Dumps a list in a file
def serializeList(file_name, list):
    with open(file_name, 'w') as convert_file:
     convert_file.write(json.dumps(list))


def main():
      
    tournamentsWithInfo = {}
    
    tournaments = getTournaments()
    tournament_names=tournaments[0]
    tournament_links=tournaments[1]
    index = 0
    
    #for every tournament, get tournament info
    for name in tournament_names:
        tournamentsWithInfo[name] = {}
        participants = getTournamentParticipants(tournament_links[index])
        matches = getTournamentMatches(tournament_links[index])
        tournamentsWithInfo[name] = {'participants':participants, 'matches':matches}

        index+=1

    serializeList('tournament_info',tournamentsWithInfo) #put info into file


   
    time.sleep(3)
    print("Done")

if __name__ == "__main__":
    main()
