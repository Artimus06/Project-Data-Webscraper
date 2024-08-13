#Imports
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import csv


projectList = []


# Set the path to the Chromedriver
service = Service(executable_path="chromedriver.exe")

chrome_options = Options()
#chrome_options.add_argument('--headless=new')
#chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--window-size=1000,700')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')





# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

#Initilize variables
marketCapNum = ''
devNum = ''
bountyRawText = ''
projectWebsite = ''

# Function to wait for page to load
def pageWait(timeout,xpath):
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        return False
    



def getMarketCap():
    # Find/print market cap
    if pageWait(3,'/html/body/div[1]/div[1]/div[2]/header[2]/div/div[2]/div[1]/div/div[3]/div/div[3]/div[2]/div[1]') == False:
        marketCapNum = 'N/A'
        return marketCapNum
    else:
        marketCap = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/header[2]/div/div[2]/div[1]/div/div[3]/div/div[3]/div[2]/div[1]')
        marketCapNum = marketCap.text
        if marketCapNum == '$ --':
            marketCapNum = 'N/A'
        return marketCapNum

def getTags():
    tagList = []
    # Find and print Tags
    if pageWait(0.5,"/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]") == False:
        print('Couldnt Find Tags')
        tagList = 'N/A'
        return tagList
    else:
        tagRow = driver.find_element(By.XPATH,"/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]")
        tags = tagRow.find_elements(By.TAG_NAME,'span')
        for tag in tags:
            tagList.append(tag.text)
        if len(tagList) > 1:
            tagList.pop(0)
        tagList = ', '.join(tagList)
        return tagList

# Find ecosystems
def getEcosystems():
    ecosystemList = []
    if pageWait(0.1,"/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]") == False:
        print("No ecosystems found")
        ecosystemList = ['blank','N/A']
        ecosystemList.pop(0)
        ecosystemList = ', '.join(ecosystemList)
    else:
        ecoRow = driver.find_element(By.XPATH,"/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]")
        ecosystems = ecoRow.find_elements(By.TAG_NAME,'span')
        # Get rid of 'soon' in list
        for i in range(len(ecosystems)):
            if ecosystems[i].text == '(soon)' or ecosystems[i].text == 'Founded:' or (ecosystems[i].text).isnumeric() == True:
                continue
            ecosystemList.append(ecosystems[i].text)
        if len(ecosystemList) == 0:
            ecosystemList = 'N/A'
            return ecosystemList
        else:
            if len(ecosystems)  == 0:
                ecosystemList = ['blank','N/A']
                ecosystemList.pop(0)
                ecosystemList = ', '.join(ecosystemList)
                return ecosystemList
            else:
                ecosystemList.pop(0)
                ecosystemList = ', '.join(ecosystemList)
                return ecosystemList

def getProjectSite():
    driver.get('https://rootdata.com')
    if pageWait(10,'/html/body/div/div/div/div/main/div/div/div/div/div/div[1]/div[1]/input') == False:
        print("Couldnt Find Project site")
        site = 'N/A'
        return site
    else:
        search_box = driver.find_element(By.XPATH,"/html/body/div/div/div/div/main/div/div/div/div/div/div[1]/div[1]/input")
        search_box.send_keys(exampleName)
        pageWait(3,'/html/body/div/div/div/div/main/div/div/div/div/div/div/div[2]/div[1]/div[1]/ul/li[1]/div/div[2]/div')
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.ENTER)
        if pageWait(1,'/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/a') == False:
            print('Couldnt find Project Website')
            site = 'N/A'
            return site
        else:
            site = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/main/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/a')
            return 'https://' +site.text


def getDevData():
    #get number of devs
    driver.get('https://www.developerreport.com')
    devSearch1 = driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/div/div[1]/div[2]/button')
    devSearch1.click()
    devSearch2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div/div/div/div/div/div/input')
    devSearch2.send_keys(exampleName)
    devSearch2.send_keys(Keys.ENTER)
    if pageWait(3,'/html/body/div/div/div[2]/div[2]/main/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[1]') == False:
        print("Couldnt find Dev Data")
        devNum = 'N/A'
        return devNum
    else:
        devNum = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div[2]/main/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[1]')
        return devNum.text







def getActiveUsers():
    driver.get('https://skynet.certik.com')
    if pageWait(5,'/html/body/div[1]/div[1]/div[2]/header[1]/div/div[1]/div/div[1]/div[1]/input') == False:
        print('Couldnt Access Certik Website')
        ActiveUsers = 'N/A'
    else:
        certikSearchBox = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/header[1]/div/div[1]/div/div[1]/div[1]/input')
        certikSearchBox.send_keys(exampleName)
        if pageWait(5,'/html/body/div[1]/div[1]/div[2]/header[1]/div/div[1]/div/div[1]/div[2]/ul/div/div[1]/div[1]/div[2]/div/a/div[2]') == False or (certikSearchBox.text).lower():
            print("Couldnt Find Project on Certik")
            ActiveUsers = 'N/A'
        else:
            certikSearchBox.send_keys(Keys.ENTER)
            if pageWait(10,'/html/body/div[1]/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[2]/span[1]') == False:
                print('Project User Data Not found')
                ActiveUsers = 'N/A'
            else:
                ActiveUsers = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[2]/span[1]')
                ActiveUsers = ActiveUsers.text
            return ActiveUsers

def getProjectAge():
    if pageWait(5, '/html/body/div[1]/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/span[1]') == False:
        print("Project Age not Found")
        projectAge = 'N/A'
    else:
        projectAge = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/span[1]')
        projectAge = projectAge.text
    return projectAge

def getLiveSince():
    liveSince = ''
    if pageWait(1,'/html/body/div[1]/div[1]/div[2]/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[1]') == False:
        print("Couldnt Find Live since data")
        liveSince = 'N/A'
        return liveSince
    else:
        liveSince = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[4]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/div[1]').text
        return liveSince

def getBountyStatus():
    bountyStatus = ''
    if pageWait(5,'/html/body/div[1]/div[1]/div[2]/div/div[4]/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div') == False:
        print("Couldnt find Bounty Status") 
        bountyStatus = 'N/A'
        return bountyStatus
    else:
        bountyStatus = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[4]/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div').text
        return bountyStatus
        

def getCertikLink():
    CertikLink  = driver.current_url
    return CertikLink











start_time = time.time()
for i in range(len(projectList)):
    if i == range(1,24):
        continue
    exampleName = projectList[i]
    finalList = []
    projectSite = getProjectSite()
    tagListstr = getTags()
    ecosystemListr = getEcosystems()
    devNum = getDevData()
    ActiveUsers = getActiveUsers()
    projectAge = getProjectAge()
    liveSince = getLiveSince()
    marketCapNum = getMarketCap()
    certikLink = getCertikLink()
    bountyStatus = getBountyStatus()
    finalList.append(exampleName)
    finalList.append(marketCapNum)
    finalList.append(ecosystemListr)
    finalList.append(tagListstr)
    finalList.append(devNum)
    finalList.append(ActiveUsers)
    finalList.append(projectAge)
    finalList.append(bountyStatus)
    finalList.append(liveSince)
    finalList.append(projectSite)
    if projectAge == 'N/A' and ActiveUsers == 'N/A':
        certikLink = 'N/A'
        finalList.append(certikLink)
    else:
        finalList.append(certikLink)

    

    #Writes all data to CSV file
    with open('output.csv', 'a', newline='', encoding="utf-8") as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        writer.writerow(finalList)
#Closes driver once the list is done   
driver.quit()
end_time=time.time()
print(end_time - start_time)

