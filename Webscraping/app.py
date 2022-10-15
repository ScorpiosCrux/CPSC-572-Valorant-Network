
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()

# IMPORTANT: Uncomment this if the page is not loading because your window is behind 
chrome_options.add_argument("--headless")

chromeDriverPath = "/Users/vivid/Code/School/CPSC-572/CPSC-572-Valorant-Network/Webscraping/chromedriver"

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









def main():

    #team_names, team_links = getTeams()
    
    #serializeList("team_links", team_links)
    team_links = readList("team_links")

    all_team_data = getAllTeamInfo(team_links)

    # Wait 3 seconds before deleting
    time.sleep(3)
    print("Done")

if __name__ == "__main__":
    main()
