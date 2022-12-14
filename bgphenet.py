import sys
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


ANSandIP = {}
ANSandIP["AS"] = []
ANSandIP["IP"] = []
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://bgp.he.net/")

timeout = int(sys.argv[2])
try:
    element_present = EC.presence_of_element_located((By.ID, 'search_search'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    elem = driver.find_element(By.ID, 'search_search')
    elem.send_keys(sys.argv[1])
    elem.send_keys(Keys.RETURN)
    if "Not Found" not in driver.page_source:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tbody = soup.find_all('tbody')
        tbody = tbody[0]
        for link in tbody.find_all('td'):
            tag_alex = link.find("a")
            if tag_alex :
                x = re.search('^AS', tag_alex.text)
                if x != None:
                    ANSandIP["AS"].append(tag_alex.text)
                else:
                    aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",tag_alex.text)
                    if aa != None:
                        ANSandIP["IP"].append(tag_alex.text)
        

        with open("bgpas.txt", "a+") as myfile:
            myfile.write("\n".join(ANSandIP["AS"]))



        with open("bgpip.txt", "a+") as myfile:
            myfile.write("\n".join(ANSandIP["IP"]))

        driver.quit()
    else:
        driver.quit()