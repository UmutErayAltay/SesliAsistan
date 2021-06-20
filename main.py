import speech_recognition as sr
import time
import speech_recognition as sr
from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyaudio
import urllib.request
import json
import requests
from pygame import mixer
from gtts import gTTS
from playsound import playsound
instagram_adi = "nick_name"
instagram_sifre = "sifre"
gmail = "e-mail"
gmail_sifre = "e-mail password"

def kapama(driver):
    döngükır=False
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("kapatma dinlemedeyim")
        audio = r.listen(source)
    try:
        metin = str(r.recognize_google(audio, language="tr"))
        if(metin.find("kapat") != -1):
            driver.close()
            döngükır = True
            return(döngükır)
    except:
        print("bir hata oldu")
def konusma(instagram_adi, instagram_sifre, gmail, gmail_sifre):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("dinlemedeyim")
        audio = r.listen(source)
    try:
        metin = str(r.recognize_google(audio,language = "tr"))
        print("dediğiniz soz: " + metin)
        if (metin.find("Instagram")!=-1):
            driver = webdriver.Opera()
            driver.get('https://www.instagram.com')
            time.sleep(1)
            username = driver.find_element_by_name("username")
            password = driver.find_element_by_name("password")
            username.send_keys(instagram_adi)
            password.send_keys(instagram_sifre)
            password.submit()
            a=True
            while (a):
                c = kapama(driver)
                if(c == True):
                    a=False
        elif(metin.find("posta")!=-1):
            driver = webdriver.Chrome()
            driver.get('https://www.gmail.com')
            username = driver.find_element_by_name("identifier")
            username.send_keys(gmail)
            time.sleep(1)
            buton = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span')
            buton.click()
            time.sleep(2)
            password = driver.find_element_by_name("password")
            password.send_keys(gmail_sifre)
            buton = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span')
            a = True
            while (a):
                c = kapama(driver)
                if (c == True):
                    a = False
    except:
        print("bir hata oldu")
while 1:
    konusma(instagram_adi, instagram_sifre, gmail, gmail_sifre)

