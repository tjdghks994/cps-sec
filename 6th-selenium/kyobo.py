from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/6th-selenium/chromedriver" # for mac
#path = os.getcwd() + "/6th-selenium/chromedriver.exe" # for window
try :
    driver = webdriver.Chrome(path)
    driver.get("http://www.kyobobook.co.kr/index.laf?OV_REFFER=https://www.google.com")
    time.sleep(1)

    searchStr = "파이썬"
    element = driver.find_element_by_class_name("main_input")
    element.send_keys(searchStr)
    driver.find_element_by_class_name("btn_search").click()

    driver.implicitly_wait(10)
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = bs.find("span", class_ = "page_jump").find("span", id = "totalpage").text
    print(pages)

    for i in range(5) :
        time.sleep(1)
        
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        cont = bs.find("div", id = "contents_section").find_all("td", class_ = "detail")
        print("\npage: ", i)
        for c in cont :
            print(c.find("div", class_ = "title").find("a").find("strong").text)

        driver.find_element_by_xpath('//*[@id="contents_section"]/div[9]/div[1]/a[3]').click()

finally :
    time.sleep(3)
    driver.quit()