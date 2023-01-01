from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re 
import json
from time import sleep
web = webdriver.Chrome()
web.get("https://keisan.casio.com/exec/system/1224682277")
#==================================================
sleep(1)
longt = 12.679056
longt_ = web.find_element(By.ID,'var_longt')
longt_.clear();
longt_.send_keys(longt)
sleep(1)
#==================================================
latit = 32.757808
latit_ = web.find_element(By.ID,'var_latit')
latit_.clear();
latit_.send_keys(latit)
sleep(1)
#==================================================
zone = 2
zone_ = web.find_element(By.ID,'var_I')
zone_.clear()
zone_.send_keys(zone)
sleep(1)
#==================================================


Submit = web.find_element(By.ID,'executebtn')
Submit.click()




html_doc = web.page_source
soup = BeautifulSoup(html_doc,  'lxml')
data = soup.find_all("script")
p = re.compile('exedata =(.*?);')
m = p.match(data[25].string)
clocks = json.loads(m.groups()[0])
del(clocks[0])
print(clocks)
