# CPSC-572 Valorant Network Analysis and Mining
Here we mined Valorant data off of Liquidpedia.com and applied various network analysis techniques to practice and aid us in solving our questions.


## Contributors
- Martha Ibarra
- Tyler Chen
- Thanh Hien Nguyen Mai

## Technology Used:
- Python
- Selenium
- Web Drivers
- Matplotlib
- Sklearn
- TensorFlow
- Seaborn
- Pandas
- Numpy
- Gephi

## Webscraping Setup Environment

### VSCode Setup 
Follow these steps closely as failing to do so make complicate things.
- With VSCode Open CPSC-572-Valorant-Network/
    - The next directory should contain at least "Webscraping"
    - Open the terminal in VSCode, your path should be something like:
        -`~/a/b/c/CPSC-572-Valorant-Network`
        - Where a, b, c doesn't really matter
    - Before you go to Virtual Environment steps, finish reading this section. 
    - You will be prompted with a little notification after creating your virtual environment.
        - Click Yes, switch to this environment.
    - When you open a python file, on your bottom bar, it should auto switch to something like `'CPSC-572-Project-VENV':venv`

### Virtual Environment

#### Creation:

- Open the cloned dir and inside create a folder and name it exactly `CPSC-572-Project-VENV` because .gitignore is configured to ignore this folder name.
`python3 -m venv /path/to/new/virtual/environment`

#### Activation:

`source CPSC-572-Project-VENV/bin/activate`

#### Installing Packages:

`pip3 install package`

#### Packages:

-   Format: package-name==version-number
-   `selenium==4.5.0`

### Drivers:

-   We need a Selenium Driver to interact with the browser. To download it, you need your Chrome Version.

##### Chrome Version:
Open Chrome -> Click the 3 dots -> Help -> About Chrome.\
You want something that looks like `Version 105.0.5195.125`\
Visit https://chromedriver.chromium.org/downloads and download the respective driver.\
Save the driver into your workspace.

#### Running Chrome Driver:
- For MacOS users, you might need to go to System Preferences - > Privacy & Security -> General Tab -> (Chrome Driver) Run Anyways


### Running demo.py
- There's a variable called `chrome_driver_path` that you need to replace with the path to where you put your chrome driver.


#### XPATH
```
1 https://liquipedia.net/valorant/index.php?title=Category:Teams
/html/body/div[3]/main/div/div[3]/div[3]/div[2]/div[2]/div/div/div[7]/ul/li[12]/a
2 https://liquipedia.net/valorant/index.php?title=Category:Teams&pagefrom=Kafalar+Esports#mw-pages
/html/body/div[3]/main/div/div[3]/div[3]/div[2]/div[2]/div/div/div[3]/ul/li[13]/a
3 https://liquipedia.net/valorant/index.php?title=Category:Teams&pagefrom=Team+nxl#mw-pages
/html/body/div[3]/main/div/div[3]/div[3]/div[2]/div[2]/div/div/div[1]/ul/li[6]/a```

