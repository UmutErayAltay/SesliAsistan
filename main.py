import speech_recognition as sr
from playsound import playsound
import smtplib
import os
gmail = "nickname@gmail.com"
gmail_sifre = "password"
def konusma(gmail, gmail_sifre):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("dinlemedeyim")
        audio = r.listen(source)
    try:
        metin = str(r.recognize_google(audio,language = "tr"))
        print("dediğiniz soz: " + metin)
        if(metin.find("posta")!=-1):
            playsound('Posta.mp3')
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(gmail, gmail_sifre)
            içerik = input("içeriği giriniz")
            alıcı = input("alıcıyı giriniz")
            print(alıcı)
            print(içerik)
            dur = input("önizleme")
            playsound('Gonder.mp3')
            mail.sendmail(gmail, alıcı, içerik)
        elif(metin.find("dur")!=-1):
            playsound('kapanis.mp3')
            return("kapat")
        elif(metin.find("opera")!=-1):
            playsound('Opera.mp3')
            os.system("start opera")
        elif (metin.find("Google Chrome") != -1):
            playsound('Chrome.mp3')
            os.system("start chrome")
        elif (metin.find("Firefox") != -1):
            playsound('Mozilla.mp3')
            os.system("start Firefox")
        elif(metin.find("Instagram")!=-1):
            playsound('instagram.mp3')
            os.system("start www.instagram.com")
        elif (metin.find("YouTube") != -1):
            playsound('YouTube.mp3')
            os.system("start www.youtube.com")
        elif (metin.find("Google") != -1):
            playsound('Google.mp3')
            os.system("start www.google.com")
    except:
        print("bir hata oldu")
döngü = True
while döngü:
    if(konusma(gmail, gmail_sifre)=="kapat"):
        döngü=False