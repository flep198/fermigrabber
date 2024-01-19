import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import glob

#url="https://fermi.gsfc.nasa.gov/ssc/data/access/lat/LightCurveRepository/source.php?source_name=4FGL_J0217.8+0144"


def getLC(url,binning="weekly",download_dir="/home/flep98/Desktop/TELAMON/FermiDownload"): #binning can be "daily","weekly" or "monthly"
    
    #check for valid input
    if binning not in ["daily","weekly","monthly"]:
        raise Exception("Please use a valid binning (daily, weekly, monthly).")
        
    if not os.path.isdir(download_dir):
        os.system("mkdir " + download_dir)
        print("Created " + download_dir + " since it did not exist.")
        
    existing_file=glob.glob(download_dir+"/"+url.split("=")[-1]+"_"+binning+"*")
    
    if len(existing_file)==0 or os.path.getsize(existing_file[0])==0:
        if len(existing_file)!=0:
            os.system("rm -rf "+existing_file[0])

        #start browser
        options=FirefoxOptions()
        options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_dir)
    
    
        driver = webdriver.Firefox(options=options)
    
    
        try:
            driver.get(url)
            driver.find_element(By.ID, binning).click()
            driver.find_element(By.XPATH, "//*[contains(text(), 'Select Format')]").click()
            driver.find_element(By.ID,"download_csv").click()
        except:
            print("Error connecting to Fermi website " + url)
        
        driver.close()
        
def downloadAll():
    
    #start browser
    options=FirefoxOptions()
    options.add_argument("--headless")
    
    
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://fermi.gsfc.nasa.gov/ssc/data/access/lat/LightCurveRepository/index.html")
        wrapper = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '4FGL J0000.5+0743')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), '100 Rows')]").click()
        driver.find_element(By.ID, "rows_all").click()
        driver.implicitly_wait(10)
        html=driver.page_source
    except:
        print("Error connecting to Fermi website " + url)
    
    soup=BeautifulSoup(html,"lxml")
    
    for link in tqdm(soup.find_all("a")):
        url=link.get("href")
        if url is not None and url.startswith("./source.html?source_name="):
            try:
                getLC("https://fermi.gsfc.nasa.gov/ssc/data/access/lat/LightCurveRepository/" + url.split("/")[1])
            except:
                print("Error with "+ url)
