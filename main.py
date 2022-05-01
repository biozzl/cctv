# -*- coding: utf-8 -*-
# https://github.com/mybdye 🌟
# BYPASS reCaptcha By YouTube Channel: NIKO TECH

import os
import sys
import time
import random
import urllib
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
urlLogin = 'https://hax.co.id/login'
SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'

# secret
try:
    USER_ID = os.environ['USER_ID']
except:
    # 本地调试用
    USER_ID = ''

try:
    PASS_WD = os.environ['PASS_WD']
except:
    # 本地调试用
    PASS_WD = ''

try:
    BARK_KEY = os.environ['BARK_KEY']
except:
    # 本地调试用
    BARK_KEY = ''

try:
    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    TG_BOT_TOKEN = ''

try:
    TG_USER_ID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    TG_USER_ID = ''

def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def reCAPTCHA():
    g_recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()

    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, "recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                # get the mp3 audio file
                # scroll down 200px
                driver.execute_script('window.scrollBy(0, 200)')
                src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFile)
                print("[INFO] Recaptcha Key: %s" % key)

                driver.switch_to.default_content()
                iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                delay()
                inputField.send_keys(Keys.ENTER)
                delay()
                delay()

                err = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    break

        except Exception as e:
            print(e)
            barkPush('[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests')
            sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        # sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
        print('reCAPTCHA not found!')
    print('reCAPTCHA done')

def CAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][0])
    caculateMethod = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][0])
    print('Method', caculateMethod)
    if caculateMethod == '+':
        captcha_result = number1 + number2
    elif caculateMethod == '-':
        captcha_result = number1 - number2
    elif caculateMethod == 'X':
        captcha_result = number1 * number2
    elif caculateMethod == '/':
        captcha_result = number1 / number2
    return captcha_result

def push(body):
    print('- waiting for push result')
    # bark push
    if BARK_KEY == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + BARK_KEY
        title = 'HaxExtend'
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')

    # tg push
    if TG_BOT_TOKEN == '' or TG_USER_ID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = 'HaxExtend\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + TG_BOT_TOKEN + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': TG_USER_ID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print(rq_tg.content.decode('utf-8'))

    print('- finish!')

try:
    # create chrome driver
    Options = webdriver.ChromeOptions()
    Options.add_argument('--headless')
    #Options.add_argument('--window-size=1920x945')
    Options.add_argument('--no-sandbox')
    Options.add_argument('--disable-gpu')
    Options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=Options)
    delay()
    # go to website which have recaptcha protection
    driver.get(urlLogin)
    delay()
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print('width,height:', width, height)
    delay()
    driver.set_window_size(width, height)
    delay()
    #driver.save_screenshot(pic_name)
    

except Exception as e:
    sys.exit(
        "[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

# main
time.sleep(10)
# scroll down
driver.execute_script('window.scrollBy(0, 500)')
delay()
print('- fill username')
driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(USER_ID)
print('- fill password')
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASS_WD)
delay()
# reCAPTCHA
print('- do reCAPTCHA')
reCAPTCHA()
time.sleep(10)
# login
driver.switch_to.default_content()
print('- click login')
driver.find_element(By.NAME, 'login').click()
time.sleep(10)
# Extend VPS link
print('- click Extend VPS')
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Extend VPS Expiration'))).click()
time.sleep(10)
# input web address
print('- fill web address')
driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys('hax.co.id')
# captcha
print('- do CAPTCHA')
driver.find_element(By.XPATH,'//*[@id="captcha"]').send_keys(CAPTCHA())
# agreement check
print('- click agreement')
driver.find_element(By.NAME, 'agreement').click()
# reCAPTCHA again
print('- do reCAPTCHA')
reCAPTCHA()
time.sleep(10)
driver.switch_to.default_content()
# submit_button (Renew VPS)
print('- click Renew VPS')
driver.find_element(By.NAME, 'submit_button').click()
time.sleep(15)
print('- copy text')
body = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
# print('textBody:', body)
delay()
print('- push')
push(body)
delay()
driver.quit()
