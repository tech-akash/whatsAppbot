
from django.http import HttpResponse
from django.shortcuts import render

from selenium import webdriver
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from whatsAppbot.settings import BASE_DIR

# client=Client(account_sid,auth_token)

def element_presence(by, xpath, time,driver):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

def send_message(url,driver):
    driver.get(url)
    time.sleep(2)
    xpath='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    element_presence(By.XPATH,xpath , 100,driver)
    msg_box = driver.find_element(By.XPATH, xpath)
    msg_box.send_keys('\n')
    time.sleep(3)

def prepare_msg(driver,name,phoneNo,msg):
    base_url = 'https://web.whatsapp.com/send?phone={}&text={}'
    for i in range(len(name)):
        url_msg = base_url.format(phoneNo[i], msg)
        print(url_msg)
        send_message(url_msg,driver)

    

def sendWhatsAppMessage(name,phoneNo,msg):
    op=webdriver.ChromeOptions()
    op.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")
    driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=op)
    
    prepare_msg(driver,name,phoneNo,msg)
    

def bot(request):
    if request.method=='POST':
        # sendWhatsAppMessage()
        name=request.POST['name'].split()
        phoneNo=request.POST['phoneNo'].split()
        msg=request.POST['msg']
        sendWhatsAppMessage(name,phoneNo,msg)
    return render(request,'form.html',{})
    
