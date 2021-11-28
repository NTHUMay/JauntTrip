

#This package helps get top rated attraction sites from Tripadvisor with a given destination. 
#It will return all destinations in a list

import re
import selenium
import io
import requests
import bs4
import urllib.request
import urllib.parse
import pandas as pd
import os



from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
#from _datetime import datetime
from selenium.webdriver.common.keys import Keys



def attraction(destination):
    print('Wait while we load data from Tripadvisor... It may take up to 1 min\n')
    options = webdriver.ChromeOptions()
    options.headless = True
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driverPath = os.path.abspath(os.getcwd()) + r'\chromedriver.exe'

    driver = webdriver.Chrome(driverPath, options = options)
    driver.maximize_window()

    url = "https://www.tripadvisor.com/"

    driver.get(url)

    time.sleep(8)
    driver.find_element_by_xpath(r'//*[@id="lithium-root"]/main/div[1]/div[2]/div/div/div[3]/a').click()
    time.sleep(10)
    driver.find_element_by_xpath(r'/html/body/div[2]/div/form/input[1]').send_keys(destination)
    time.sleep(10)
    driver.find_element_by_xpath(r'/html/body/div[2]/div/form/input[1]').send_keys(Keys.ENTER)


    time.sleep(10)

    url = driver.current_url

    response = driver.page_source
    
    data = bs4.BeautifulSoup(response, 'lxml')
    read1 = data.select(".title")
    titles = data.find_all("div", {"class": "bUshh o csemS"})
    destinationList = []

    for item in titles:
        destinationList.append(item.text)
    
    return destinationList

def displayAttraction(attractionList, pageNum):
    
    if pageNum < 1:
        pageNum = 1
    
    numAttractions = len(attractionList)
    
    # change this if needed
    itemsPerPage = 5
    
    lastItem = pageNum * itemsPerPage
    firstItem = lastItem - itemsPerPage
    
    if lastItem > numAttractions:
        lastItem = numAttractions
        
    if firstItem < 0:
        firstItem = 0
        
    toPrint = attractionList[firstItem:lastItem]
    
    if toPrint == []:
        print("You have checked through all the touristic sites!")
    else:
        for item in toPrint:
            print(item)
    