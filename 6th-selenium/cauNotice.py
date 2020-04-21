from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th-selenium/chromedriver" # for mac
#path = os.getcwd() + "/6th-selenium/chromedriver.exe" # for window
driver = webdriver.Chrome(path)
driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page1")

req = driver.page_source
bs = BeautifulSoup(req, "html.parser")

# total page
pages = bs.find("div", class_ = "pagination").find_all("a")[-1]["href"] # "#page21"
pages = pages.split("page")[-1]
pages = int(pages)

title = []
try :
    for i in range(pages) :
        driver.get("https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=2130#page" + str(i + 1))    
        
        time.sleep(2)

        req = driver.page_source
        bs = BeautifulSoup(req, "html.parser")

        contents = bs.find_all("div", class_ = "txtL")

        title.append("page" + str(i + 1))
        for c in contents :
            title.append(c.find("a").text)
finally :
    driver.quit()

for t in title :
    if t.find("page") != -1 :
        print()
        print(t)
    else :
        print(t)