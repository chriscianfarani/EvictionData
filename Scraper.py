from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import lxml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def get_info(soup, info):
    text = soup.find(class_="text-muted", string=info).find_parent('p')
    unwanted = text.find('span')
    unwanted.extract()
    return text

def get_info_parties(soup, name):
    text = soup.find(class_='text-primary', string=re.compile(name)).find_parent('p')
    unwanted = text.find('span')
    unwanted.extract()
    return text

year = '2011'

driver = webdriver.Chrome('/Users/christiancianfarani/cdriver/chromedriver')
driver.implicitly_wait(30)
driver.get('https://publicportal.courts.ri.gov/PublicPortal/Home/Dashboard/29')
searchbox = driver.find_element_by_id('caseCriteria_SearchCriteria')
searchbox.send_keys('6CA-2011-020*')
searchbutton = driver.find_element_by_id('btnSSSubmit')
searchbutton.click()

rows_list = []

try:
    for batch in range(21,135):
        cont = True
        while(cont):
            ls = driver.find_elements_by_class_name("caseLink")
            for case in ls:
                dict1 = {}
                case.click()
                back = driver.find_element_by_id("tcControllerLink_1")
            
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "PortletSummaryROA")))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "divPartyInformation_body")))

                soup = BeautifulSoup(driver.page_source, 'lxml')
            
                text = get_info(soup, "Case Type")
                case_type = text.get_text(strip=True)
                if(bool(re.search('Eviction', case_type))):
                    #print(case_type)
                    dict1['CaseType'] = case_type

                    text = get_info(soup, "Case Number")
                    case_num = text.get_text(strip=True)
                    dict1['CaseNum'] = case_num
                    #print(case_num)
                    text = get_info(soup, "File Date")
                    date = text.get_text(strip=True)
                    dict1['Date'] = date
                    #print(date)

                    #plaintiff = get_info_parties(soup, "Plaintiff")
                    #defendant = get_info_parties(soup, "Defendant")
                    #plaintiff = soup.find(class_="text-primary", string=re.compile("Plaintiff"))
                    #plaintiff = plaintiff.find_parent('p')
                    """
                    ls = soup.find_all(class_="text-primary")
                    plaintiff = ls[2].find_parent('p')
                    defendant = ls[4].find_parent('p')
                    unwanted = plaintiff.find('span')
                    unwanted.extract()
                    unwanted2 = defendant.find('span')
                    unwanted2.extract()
                    plaintiff = plaintiff.get_text(strip=True)
                    defendant = defendant.get_text(strip=True)
                    dict1['Plaintiff'] = plaintiff
                    dict1['defendant'] = defendant
                    print("Plaintiff: " + plaintiff)
                    print("Defendant: " + defendant)
                    """
                    location = soup.find(class_="tyler-color-muted", string=re.compile("Property Location"))
                    if location is not None:
                        location = location.find_parent('p')
                        unwanted = location.find('span')
                        unwanted.extract()
                        loc = location.get_text(strip=True)
                        dict1['Address'] = loc
                        #print(loc)
                    
                    rows_list.append(dict1)
                    #print()
                
                back.click()

            soup = BeautifulSoup(driver.page_source, 'lxml')
            next_page_soup = soup.find(class_='k-link k-state-disabled', href='/PublicPortal/SmartSearch/SmartSearchResults?CasesGrid-page=2')

            next_page = driver.find_element_by_link_text('arrow-e')

            if next_page_soup is None:
                next_page.click()
            else:
                cont = False
        driver.get('https://publicportal.courts.ri.gov/PublicPortal/Home/Dashboard/29')
        searchbox = driver.find_element_by_id('caseCriteria_SearchCriteria')
        searchbox.clear()
        searchbox.send_keys('6CA-2011-' + str(batch).zfill(3) + '*')
        searchbutton = driver.find_element_by_id('btnSSSubmit')
        searchbutton.click()
except:
    print("Error")

filename = 'data' + year + time.strftime("%Y%m%d-%H%M%S") + '.csv'
df = pd.DataFrame(rows_list)
df.to_csv(filename)
