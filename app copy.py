from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import os
import webbrowser
import subprocess
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from pathlib import Path

# .env dosyasından API anahtarını yükle
load_dotenv()

# Kısayollar klasörü
SHORTCUTS_DIR = "shortcuts"
shortcuts_dict = {}

class ShortcutHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            update_shortcuts()
    
    def on_deleted(self, event):
        if not event.is_directory:
            update_shortcuts()
    
    def on_modified(self, event):
        if not event.is_directory:
            update_shortcuts()

def update_shortcuts():
    """Kısayollar klasöründeki dosyaları günceller"""
    shortcuts_dict.clear()
    for file in Path(SHORTCUTS_DIR).glob('*'):
        if file.is_file():
            shortcuts_dict[file.stem.lower()] = str(file)
    print("\nKısayollar güncellendi!")

def setup_voice():
    """Ses motorunu başlatır"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    # Türkçe ses varsa onu seç
    for voice in voices:
        if "turkish" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

def speak(engine, text):
    """Metni seslendirir"""
    print(f"Asistan: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Mikrofondan ses alır ve metne çevirir"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nSizi dinliyorum...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
    try:
        text = r.recognize_google(audio, language='tr-TR')
        print(f"\nSiz: {text}")
        return text
    except sr.UnknownValueError:
        return "DINLEME_HATASI"
    except sr.RequestError:
        return "BAGLANTI_HATASI"

def create_chat_model():
    # Gemini modelini başlat
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    return llm

def execute_command(command):
    try:
        if command.startswith("cmd:"):
            # CMD komutu çalıştır
            cmd = command[4:].strip()
            subprocess.Popen(cmd, shell=True)
            return f"Komut çalıştırıldı: {cmd}"
        
        elif command.startswith("web:"):
            # Web sitesi aç
            url = command[4:].strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return f"Website açıldı: {url}"
        
        elif command.startswith("shortcut:"):
            # Kısayol aç
            shortcut = command[9:].strip().lower()
            if shortcut in shortcuts_dict:
                subprocess.Popen([shortcuts_dict[shortcut]], shell=True)
                return f"Kısayol açıldı: {shortcut}"
            return f"Kısayol bulunamadı: {shortcut}"
        
        else:
            return "Geçersiz komut formatı"
            
    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        return "Komut çalıştırılırken hata oluştu"

def main():
    print("Gemini AI Asistan")
    print("Komutlar:")
    print("- 'komut' diyerek bir görev verebilirsiniz")
    print("- 'sohbet' diyerek sohbet moduna geçebilirsiniz")
    print("- 'kısayollar' diyerek mevcut kısayolları görebilirsiniz")
    print("Çıkmak için 'çıkış' deyin")
    print("-" * 50)

    # Kısayollar klasörünü oluştur ve izle
    os.makedirs(SHORTCUTS_DIR, exist_ok=True)
    update_shortcuts()
    
    # Klasör değişikliklerini izle
    event_handler = ShortcutHandler()
    observer = Observer()
    observer.schedule(event_handler, SHORTCUTS_DIR, recursive=False)
    observer.start()

    llm = create_chat_model()
    memory = ConversationBufferMemory(return_messages=True)

    # Ana sistem şablonu
    system_prompt = ChatPromptTemplate.from_messages([
        ("system", """Sen gelişmiş bir asistansın. Kullanıcının isteğine göre iki modda çalışabilirsin:

1. Komut Modu:
Kullanıcı "komut" dediğinde, verilen görevi analiz edip uygun komutu üretmelisin.
Yanıtını şu formatlardan biriyle vermelisin:
- cmd:komut -> Windows komut satırı komutu
- web:adres -> Web sitesi açma
- shortcut:isim -> Kısayol açma

Örnekler:
- "Chrome'u aç" -> "shortcut:chrome"
- "youtube.com'u aç" -> "web:youtube.com"
- "notepad aç" -> "cmd:notepad"
- "hesap makinesini aç" -> "cmd:calc"

2. Sohbet Modu:
Kullanıcı "sohbet" dediğinde, normal bir sohbet asistanı gibi davranmalısın.
Yanıtını doğal bir şekilde vermelisin.

3. Kısayol Listesi:
Kullanıcı "kısayollar" dediğinde, "LIST_SHORTCUTS" yanıtını vermelisin.

Her kullanıcı girdisi için önce mod kontrolü yapmalısın."""),
        ("human", "{input}")
    ])

    # Zinciri oluştur
    chain = system_prompt | llm

    current_mode = None

    while True:
        user_input = listen()
        
        if user_input == "DINLEME_HATASI":
            print("Üzgünüm, sizi anlayamadım. Tekrar söyler misiniz?")
            continue
        elif user_input == "BAGLANTI_HATASI":
            print("Üzgünüm, bir bağlantı hatası oluştu.")
            continue
        
        if user_input.lower() in ['çıkış', 'çık', 'kapat']:
            print("Görüşmek üzere!")
            break

        try:
            # Mod kontrolü
            lower_input = user_input.lower()
            if lower_input == "komut":
                current_mode = "komut"
                print("\nKomut moduna geçildi. Görevinizi söyleyin.")
                continue
            elif lower_input == "sohbet":
                current_mode = "sohbet"
                print("\nSohbet moduna geçildi. Benimle sohbet edebilirsiniz.")
                continue
            elif lower_input == "kısayollar":
                if shortcuts_dict:
                    print("\nMevcut kısayollar:")
                    for shortcut in shortcuts_dict.keys():
                        print(f"- {shortcut}")
                else:
                    print("\nHenüz hiç kısayol eklenmemiş.")
                continue

            # Mod yoksa uyarı ver
            if not current_mode:
                print("\nLütfen önce bir mod seçin (komut/sohbet)")
                continue

            # Gemini'ye gönder
            response = chain.invoke({"input": f"{current_mode}:{user_input}"})
            
            if current_mode == "komut":
                if response.content == "LIST_SHORTCUTS":
                    if shortcuts_dict:
                        print("\nMevcut kısayollar:")
                        for shortcut in shortcuts_dict.keys():
                            print(f"- {shortcut}")
                    else:
                        print("\nHenüz hiç kısayol eklenmemiş.")
                else:
                    result = execute_command(response.content)
                    print("\nSonuç:", result)
            else:  # sohbet modu
                print("\nCevap:", response.content)
            
            # Sohbet geçmişini güncelle
            memory.save_context({"input": user_input}, {"output": response.content})
            
        except Exception as e:
            print(f"\nHata oluştu: {str(e)}")

    # İzleyiciyi durdur
    observer.stop()
    observer.join()

if __name__ == "__main__":
    main() 