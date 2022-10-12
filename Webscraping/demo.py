from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import time

chrome_driver_path = "/Users/vivid/Code/School/CPSC-572/CPSC-572-Valorant-Network/Webscraping/chromedriver"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)


#Get the URL, you can add exception handling here or even assertions
def getURL(url):
    driver.get(url)



def main():
    getURL("https://liquipedia.net/valorant/Main_Page")

    # Wait 3 seconds before deleting
    time.sleep(3)
    print("Done")

if __name__ == "__main__":
    main()
