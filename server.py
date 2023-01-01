import ntplib 
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from time import ctime
from re import compile
import numpy as np
from requests import get
def find_nearest(array, str_time):
    value = int(str_time)
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def send_rotation(azm , elev,min_az,max_az):
    azm = float(azm)
    elev = float(elev)
    #MY LASTEST CALCULATION SAY THAT THIS SHIT IS PERFECT SORRY NO IT IS NOT
    #i_angle = abs(180 - float(azm))
    #equation      needed angle / 2 -  sun_angle 
    #now this is what we call perfect calculations
    
    if(azm <=90):
        i_angle = translate(azm , min_az , 180 ,0,90)
    if(azm >=90):
        i_angle = translate(azm ,180, max_az ,90,180)
        
    if(i_angle> 0 and i_angle < 185):
        m_angle = (60 - i_angle ) / 2
        fm_angle = (m_angle - 90) * -1
        
    e_angle = (60 - elev ) / 2
    fe_angle = (e_angle - 90) * -1
    print(azm)
    print(i_angle)
    print(fm_angle)
    print(elev)
    
    try:
        req = get("https://blynk.cloud/external/api/update?token=xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV&v2={}".format(elev))
        req = get("https://blynk.cloud/external/api/update?token=xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV&v3={}".format(azm))
        req = get("https://blynk.cloud/external/api/update?token=xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV&v4={}".format(fm_angle))
        req = get("https://blynk.cloud/external/api/update?token=xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV&v5={}".format(fe_angle))
    except:
        pass
        
def cur_time():
    done = False
    counter = 0
    while(not done):
        if(counter<5):
            try:
                ntp_client = ntplib.NTPClient()
                response = ntp_client.request('pool.ntp.org')
                counter += 1
                return ctime(response.tx_time)[11:16]
            except:
                pass
        else:
            break

curr_time = cur_time()        

web = webdriver.Chrome()
web.get("https://keisan.casio.com/exec/system/1224682277")

sleep(1)

longt = 12.679056
longt_ = web.find_element(By.ID,'var_longt')
longt_.clear();
longt_.send_keys(longt)
sleep(1)
latit = 32.757808
latit_ = web.find_element(By.ID,'var_latit')
latit_.clear();
latit_.send_keys(latit)
sleep(1)

zone = 2
zone_ = web.find_element(By.ID,'var_I')
zone_.clear()
zone_.send_keys(zone)
sleep(1)

Submit = web.find_element(By.ID,'executebtn')
Submit.click()

html_doc = web.page_source
soup = BeautifulSoup(html_doc,  'lxml')
data = soup.find_all("script")
p = compile('exedata =(.*?);')
m = p.match(data[25].string)
clocks = json.loads(m.groups()[0])
del(clocks[0])    
print(curr_time)
min_list = []
hours_list = []
text_time_list = []
elev_list = []
azm_list = []

for time in clocks:
    site_min = int(time[0][3:5])
    site_hour = int(time[0][:2])
    #print("{}:{}".format(site_hour,site_min))
    min_list.append(site_min)
    hours_list.append(site_hour)
    text_time_list.append(time[0])
    elev_list.append(time[1])
    azm_list.append(time[2])

elev_list = [float(x) for x in elev_list]
#azm_list = [float(x) for x in azm_list] 
azm_bound = []

for i , elev in enumerate(elev_list):
    if (int(elev) == 0):
        azm_bound.append(float(clocks[i][2]))
        print(clocks[i][2])
        
while(True):
    curr_time = cur_time()   
    print(curr_time[:2])
    print(curr_time[3:5])
    nearest_hour = find_nearest(hours_list , curr_time[:2])
    nearest_min = find_nearest(min_list ,curr_time[3:5])
    print("nearest time {}:{}".format(nearest_hour,nearest_min))
    if (nearest_min == 0):
        nearest_min = "00"
    if (nearest_hour == 0):
        nearest_hour = "00"
    if (nearest_hour == 1):
        nearest_hour = "01"
    if (nearest_hour == 2):
        nearest_hour = "02"
    if (nearest_hour == 3):
       nearest_hour = "03"
    
    t_idx = text_time_list.index("{}:{}".format(nearest_hour,nearest_min))
    send_rotation(clocks[t_idx][2],clocks[t_idx][1] , azm_bound[0] , azm_bound[-1])
    sleep(30)
    
#for i , angle in enumerate(azm_list):
#    if(angle <=90):
#        i_angle = translate(angle , 118 , 180 ,0,90)
#    if(angle >=90):
#        i_angle = translate(angle ,180, 243 ,90,180)
#    if(i_angle> 0 and i_angle < 185):
#        m_angle = (60 - i_angle ) / 2
#        fm_angle = (m_angle - 90) * -1)
#        print("{} --- {} --- {} --- {}".format(clocks[i][0], angle ,int(i_angle) , )

    #e_angle = (60 - elev ) / 2
    #fe_angle = (m_angle - 90) * -1
    #print("{} --- {} --- {} --- {}".format(clocks[i][0], elev , m_angle,fm_angle))
    