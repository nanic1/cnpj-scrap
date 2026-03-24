from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd

today = datetime.today()

driver = webdriver.Chrome()
url = "http://cnpj.info/"
driver.get(url)

cnpj = driver.find_element(By.XPATH, '/html/body/div[1]/form/h3/input[1]')
cnpj.send_keys("01268958000120")
driver.find_element(By.XPATH, "/html/body/div[1]/form/h3/input[2]").click()
driver.implicitly_wait(5)


cnpjheader = driver.find_element(By.XPATH, '//*[@id="content"]/table[1]/tbody/tr[1]/td[1]')
print(cnpjheader.text)

driver.quit()