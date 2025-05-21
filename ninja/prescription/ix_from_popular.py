from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

driver.get("https://www.populardiagnostic.com/our-price-list/1/0")
time.sleep(10)
for i in range(2,30):
    tds = driver.find_elements(By.TAG_NAME,"td")

    for i in range(2,len(tds),4):
        with open('ix_list.txt','a') as file:
            file.write(tds[i].text+"\n")

    next_id = driver.find_elements(By.CLASS_NAME,"page-link")[8]
    next_id.click()