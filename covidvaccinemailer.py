from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options

#code to run in headless mode:
chrome_options=Options()
chrome_options.add_argument('--headless')

url='https://www.cowin.gov.in/'
driver=webdriver.Chrome(service=Service('C:\webdrivers\chromedriver.exe'),options=chrome_options)  # specify path for chromedriver
driver.get(url)
driver.maximize_window()
time.sleep(2)

for i in range(0,5):
    try:
        pinclick=driver.find_element(By.XPATH,value='//*[@id="mat-tab-label-1-1"]')
        time.sleep(2)
        pinclick.click()
        time.sleep(0.5)
    except:
        pass

pincode='670644'      #enter your pincode here

pinbar=driver.find_element(By.XPATH,value='//*[@id="mat-input-0"]')
pinbar.click()
pinbar.send_keys(pincode) #enter pincode here
pin_search=driver.find_element(By.XPATH,value='//*[@id="mat-tab-content-1-1"]/div/div[1]/div/div/button')
pin_search.click()
time.sleep(1)


for i in range(0,5):
    hospital_name=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div[1]/div/h5')
    hospital_address=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div[1]/div/p')
    doses_today=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div[2]/ul/li[1]/div/h5')
    vaccine_manufa=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div[1]/div/div/p[1]')
    ages=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div/div/div/p[2]/span[1]')
    dose_no=driver.find_elements(By.XPATH,value='/html/body/app-root/div/section/app-home/div[7]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[5]/div[2]/div/div/div/div/div/div[1]/div/div/p[2]/span[2]')
    time.sleep(0.3)
    
hospi_list=[]
hospi_address_list=[]
doses_today_list=[]
vaccine_manu_list=[]
ages_list=[]
which_dose_list=[]

for hospital in hospital_name:
    hospi_list.append(hospital.text)
for address in hospital_address:
    hospi_address_list.append(address.text)
for doses in doses_today:
    doses_today_list.append(doses.text)
for manufacturer in vaccine_manufa:
    vaccine_manu_list.append(manufacturer.text)
for age in ages:
    ages_list.append(age.text)
for doseno in dose_no:
    which_dose_list.append(doseno.text)
time.sleep(0.5)

dictionary={'Hospital Name':hospi_list,
            'Hospital Address':hospi_address_list,
            'Number of doses available today':doses_today_list,
            'Vaccine Manufacturer':vaccine_manu_list,
            'For ages':ages_list,
            'Dose':which_dose_list}


time.sleep(0.2)

for i in range(0,6):
    try:
        df=pd.DataFrame.from_dict(dictionary)
        time.sleep(0.2)
    except:
        pass

df['Dose']=df['Dose'].apply(lambda x: x.replace('Dose: ',''))
df['For ages']=df['For ages'].apply(lambda x: x.replace('Age: ',''))



msg = MIMEMultipart()
msg['Subject'] = "Vaccines available at selected pincode: " + pincode
msg['From'] = 'Automated Script'


html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(df.to_html(index=False))

part1 = MIMEText(html, 'html')
msg.attach(part1)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('yourmailhere@gmail.com', 'yourpasswordhere')   #enter your username and password here, also allow access for less secure apps from google security
server.sendmail(msg['From'], 'destination_mail@gmail.com' , msg.as_string()) 



