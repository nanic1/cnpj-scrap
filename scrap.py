# app encontra-se com erro pois sites disponiveis para scrap estão com proteção de dados

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time
import random

today = datetime.today()

driver = webdriver.Chrome()
url = "http://cnpj.info/"
driver.get(url)

cnpj_list = [
    "11398351000119", "01268958000120"
]

wait = WebDriverWait(driver, 10)

for cnpj_value in cnpj_list:
    for i in range(2):
        input_cnpj = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/h3/input[1]'))
        )

        time.sleep(random.randint(3, 8))
        
        input_cnpj.clear()
        input_cnpj.send_keys(cnpj_value)
        time.sleep(random.randint(3, 8))
        input_cnpj.send_keys(Keys.ENTER)
    
    table = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/table'))
    )
    
    print(f"\nResultados para CNPJ: {cnpj_value}")
    
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        data = [column.text for column in columns]
        print(data)
    
    # voltar para página anterior
    driver.back()

driver.quit()