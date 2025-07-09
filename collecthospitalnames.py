from selenium import webdriver
from selenium.webdriver.common.by import By
import time

geckodriver_path = "/snap/bin/geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=driver_service)
#driver = webdriver.Firefox()
driver.get("http://103.247.238.81/hsmdghs/registration/hsm_facility_show_public.php")
time.sleep(20)

data_list = []
for i in range(1,181):
    try:
        tdlist = driver.find_elements(By.TAG_NAME, "td")
        for j in range(len(tdlist)):
            if (j%8 == 0) or (j == 0):
                new_data = [
                    tdlist[j+1].text,
                    tdlist[j+2].text,
                    tdlist[j+3].text,
                    tdlist[j+4].text,
                    tdlist[j+5].text,
                    tdlist[j+6].text,
                    tdlist[j+7].text,
                ]
                data_list.append(new_data)
            else:
                pass
        print(len(data_list))
        try:
            next = driver.find_element(By.LINK_TEXT,"Next")
            next.click()
        except:
            pass
        time.sleep(3)
    except:
        with open('hospitals_database.txt', 'a', encoding='utf-8') as f:
            for data in data_list:
                f.write(f"{data}\n")
driver.quit()

with open('hospitals_database.txt', 'a', encoding='utf-8') as f:
    for data in data_list:
        f.write(f"{data}\n")
