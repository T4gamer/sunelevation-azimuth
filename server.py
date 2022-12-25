from selenium import webdriver
from selenium.webdriver.common.by import By
import time

web = webdriver.Chrome()
web.get("https://keisan.casio.com/exec/system/1224682277")

time.sleep(1)

longt = 32.757808
longt_ = web.find_element(By.ID,'var_longt')
longt_.clear();
longt_.send_keys(longt)
time.sleep(1)
latit = 12.679056
latit_ = web.find_element(By.ID,'var_latit')
latit_.clear();
latit_.send_keys(latit)
time.sleep(1)

zone = 2
zone_ = web.find_element(By.ID,'var_I')
zone_.clear()
zone_.send_keys(zone)
time.sleep(1)

Submit = web.find_element(By.ID,'executebtn')
Submit.click()
input("enter any key")
angles = web.find_elements(By.CLASS_NAME,'htDimmed')

for angle in angles:
    print(angle.text)
input("enter any key")