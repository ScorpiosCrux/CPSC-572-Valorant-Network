# Webscraping Setup Environment

## VSCode Setup 
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

## Virtual Environment

### Creation:

Create a folder and name it exactly `CPSC-572-Project-VENV` because .gitignore is configured to ignore this folder name.
`python3 -m venv /path/to/new/virtual/environment`

### Activation:

`source CPSC-572-Project-VENV/bin/activate`

### Installing Packages:

`pip3 install package`

### Packages:

-   Format: package-name:version-number
-   `selenium:4.5.0`

## Drivers:

-   We need a Selenium Driver to interact with the browser. To download it, you need your Chrome Version.

#### Chrome Version:
Open Chrome -> Click the 3 dots -> Help -> About Chrome.\
You want something that looks like `Version 105.0.5195.125`\
Visit https://chromedriver.chromium.org/downloads and download the respective driver.\
Save the driver into your workspace.

## Running Chrome Driver:
- For MacOS users, you might need to go to System Preferences - > Privacy & Security -> General Tab -> (Chrome Driver) Run Anyways



