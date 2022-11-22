from urllib import request
from bs4 import BeautifulSoup as bsp
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import os
import json
import re




class Scanner:
    driver = None

    def __init__(self, driver=None):
        # self.driver = driver
        if not driver:
            options = Options()
            options.headless = True
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = driver


    def getAbi(self, address):
        try:
            filename = f'ABI_{address}.txt'
            with open(f"data/{filename}") as f:
                abi = f.readlines()
                if (len(abi) == 0 & os.path.exists(f"data/{filename}")):
                    os.remove("data/{filename}")
                    self.getAbi(address)
                return abi[0]
        except IOError:
            abi = findAbi_driver(address, self.driver)
            return abi

    def getTokenTracker(self, address):
        url = f'https://bscscan.com/token/{address}'
        self.driver.get(url)
        page_soup = bsp(self.driver.page_source, features="lxml")
        tracker = page_soup.find_all("span", {"class": "text-secondary small"})[0].text
        return tracker

def findAbi(address, driver):
    response = requests.get(f'https://api.bscscan.com/api?module=contract&action=getabi&address={address}&apiKey=7D44HWWM2V4GM7ZBR1P9Y38A2ERNHSD1Z1')
    abi = json.loads(response.text)['result']

    with open(f'data/ABI_{address}.txt', 'w') as f:
        f.write(abi)

    return abi

def findAbi_driver(address, driver):
    # url = f'https://bscscan.com/address/{address}#code'
    url = f'https://testnet.bscscan.com/address/{address}#code'

    if not driver:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    driver.get(url)
    page_soup = bsp(driver.page_source, features="lxml")
    abi = page_soup.find_all("pre", {"class": "wordwrap js-copytextarea2"})[0].text
    # response = requests.get(f'https://api.bscscan.com/api?module=contract&action=getabi&address={address}&apiKey=7D44HWWM2V4GM7ZBR1P9Y38A2ERNHSD1Z1')
    # abi = json.loads(response.text)['result']

    with open(f'data/ABI_{address}.txt', 'w') as f:
        f.write(abi)

    driver.delete_all_cookies()
    # driver.get("chrome://settings/clearBrowserData");
    # driver.close()
    return abi