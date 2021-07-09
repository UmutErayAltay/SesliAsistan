import speech_recognition as sr
from playsound import playsound
import datetime
from gtts import gTTS
import smtplib
import os
gmail = ".....@gmail.com"
gmail_sifre = "............"
def konusma(gmail, gmail_sifre):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("dinlemedeyim boss")
        audio = r.listen(source)
    try:
        metin = str(r.recognize_google(audio,language = "tr"))
        print("dediğiniz soz: " + metin)
        metin = metin.lower()
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
        elif (metin.find("uyku modu") != -1):
            playsound("PCUykuModunda.mp3")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif (metin.find("league of legends kapat") != -1):
            playsound("LOLKapaniyor.mp3")
            os.system("taskkill /IM LeagueClientUx.exe")
            os.system("taskkill /IM LeagueClientUx.exe")
        elif (metin.find("bilgisayarı kapat") != -1):
            playsound("PCKapaniyor.mp3")
            os.system("shutdown -s -f -t 3")
        elif (metin.find("valorant kapat") != -1):
            playsound("ValorantKapaniyor.mp3")
            os.system("taskkill /IM VALORANT-Win64-Shipping.exe")
        elif (metin.find("spotify kapat") != -1):
            playsound("SpotifyKapaniyor.mp3")
            os.system("taskkill /IM spotify.exe")
        elif (metin.find("operayı kapat") != -1):
            playsound("operakapaniyor.mp3")
            os.system("taskkill /IM opera.exe")
        elif (metin.find("google chrome kapat") != -1):
            playsound("GoogleChromeKapaniyor.mp3")
            os.system("taskkill /IM chrome.exe")
        elif (metin.find("mozilla kapat") != -1):
            playsound("MozillaKapaniyor.mp3")
            os.system("taskkill /IM Firefox.exe")
        elif(metin.find("uygulamayı kapat")!=-1):
            playsound('kapanis.mp3')
            return("kapat")
        elif(metin.find("opera")!=-1):
            playsound('Opera.mp3')
            os.system("start Opera.lnk")
        elif (metin.find("google chrome") != -1):
            playsound('Chrome.mp3')
            os.system("start chrome")
        elif (metin.find("mozilla") != -1):
            playsound('Mozilla.mp3')
            os.system("start Firefox")
        elif(metin.find("instagram")!=-1):
            playsound('instagram.mp3')
            os.system("start www.instagram.com")
        elif (metin.find("youtube") != -1):
            playsound('YouTube.mp3')
            os.system("start www.youtube.com")
        elif (metin.find("google") != -1):
            playsound('Google.mp3')
            os.system("start www.google.com")
        elif (metin.find("league of legends") != -1):
            playsound("LoL.mp3")
            os.system('start League_of_Legends.lnk')
        elif (metin.find("valorant") != -1):
            playsound("Valorant.mp3")
            os.system('start VALORANT.lnk')
        elif (metin.find("discord") != -1):
            playsound("Discord.mp3")
            os.system('start Discord.lnk')
        elif (metin.find("steam") != -1):
            playsound("Steam.mp3")
            os.system('start Steam.lnk')
        elif (metin.find("mesaj kutusu") != -1):
            playsound('MesajKutusu.mp3')
            os.system("start https://www.instagram.com/direct/inbox/")
        elif (metin.find("spotify") != -1):
            playsound('Spotify.mp3')
            os.system("start spotify")
        elif (metin.find("whatsapp") != -1):
            playsound('WhatsApp.mp3')
            os.system("start https://web.whatsapp.com")
        elif (metin.find("saat") != -1):
            an = datetime.datetime.now()
            yıl = an.year.__str__()
            ay = an.month.__str__()
            gün = an.day.__str__()
            saat = an.hour.__str__()
            dakika = an.minute.__str__()
            tarih = yıl + ay + gün + dakika
            tts = gTTS(text="saat" + saat + "," + dakika, lang='tr')
            ses_kaydı = tarih + ".mp3"
            tts.save(ses_kaydı)
            playsound(ses_kaydı)
    except:
        print("bir hata oldu")
döngü = True
döngü2 = True
while döngü:
    if(konusma(gmail, gmail_sifre)=="kapat"):
        döngü=False