from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
import subprocess
import webbrowser
from dotenv import load_dotenv
from shortcuts_manager import shortcuts_dict
from spotify_manager import SpotifyManager  # SpotifyManager'ı içe aktar
import psutil
import win32gui
import win32process
# .env dosyasından API anahtarını yükle
load_dotenv()

def enum_window_callback(hwnd, visible_pids):
    # Pencere görünür mü ve pencere başlığı boş değilse kontrol et
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd).strip():
        # Pencerenin hangi işleme ait olduğunu al
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        visible_pids.add(pid)

def get_foreground_applications():
    visible_pids = set()
    # Tüm üst düzey pencereleri gez ve visible_pids kümesine PID'leri ekle
    win32gui.EnumWindows(enum_window_callback, visible_pids)

    app_names = set()
    for pid in visible_pids:
        try:
            proc = psutil.Process(pid)
            # İşlemin adı (örneğin "chrome.exe", "notepad.exe") alınır
            app_names.add(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return list(app_names)

def create_chat_model():
    """Gemini modelini başlatır"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    return llm

def create_task_chain(llm):
    """Görev zincirini oluşturur"""
    uygulamalar = get_foreground_applications()
    print(uygulamalar)
    task_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
        close komutu için açık olan uygulamaların isimleri :
        {uygulamalar} 
        Sen bir görev analiz asistanısın. Kullanıcının isteklerini analiz edip uygun komutu üretmelisin.
        Sen büyük bir dil modelinden ziyade sesli bir asistansın ve alt kısımda verilmiş komutları yazarak işlemleri yerine getiriyorsun.
        Yanıtını aşağıdaki formatlardan birinde, **yalnızca komut olacak şekilde** vermelisin:
        
        - cmd:<komut> → Windows komut satırında çalıştırılacak komut
        - web:<adres> → Web tarayıcısında açılacak site
        - shortcut:<isim> → Bilgisayardaki bir kısayolu açma
        - close:<uygulama_adı> → Belirtilen uygulamayı kapatma
        - music:<şarkı_adı> → Spotify'da şarkıyı çal
        - music_control:<komut> → Spotify'da müzik kontrolü (pause, resume, next, previous)
        
        Örnekler:
        - Kullanıcı: "Chrome'u aç" → Yanıt: shortcut:Chrome
        - Kullanıcı: "Google'ı aç" → Yanıt: web:https://www.google.com
        - Kullanıcı: "Komut satırını aç" → Yanıt: cmd:cmd
        - Kullanıcı: "Spotify'ı kapat" → Yanıt: close:Spotify
        - Kullanıcı: "Imagine Dragons - Believer çal" → Yanıt: music:Imagine Dragons - Believer
        - Kullanıcı: "Şarkıyı durdur" → Yanıt: music_control:pause
        
        Sadece yukarıdaki formatlardan birini kullanarak yanıt ver."""), 
        ("human", "{input}")
    ])
    return task_prompt | llm

def create_chat_chain(llm):
    """Sohbet zincirini oluşturur"""
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen yardımcı bir asistansın. Sorulara açık ve anlaşılır şekilde cevap ver."),
        ("human", "{input}")
    ])
    return chat_prompt | llm

def execute_command(command):
    """Komutları çalıştırır"""
    try:
        if command.startswith("cmd:"):
            # CMD komutu çalıştır ve çıktıyı yakala
            cmd = command[4:].strip()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"Komut çalıştırıldı: {cmd}\nÇıktı:\n{result.stdout}"
            else:
                return f"Komut çalıştırılırken hata oluştu: {cmd}\nHata:\n{result.stderr}"

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
                try:
                    subprocess.Popen([shortcuts_dict[shortcut]], shell=True)
                    return f"Kısayol açıldı: {shortcut}"
                except Exception as e:
                    return f"Kısayol çalıştırılırken hata oluştu: {str(e)}"
            return f"Kısayol bulunamadı: {shortcut}"

        elif command.startswith("close:"):
            # Uygulamayı kapat
            app_name = command[6:].strip().lower()
            try:
                os.system(f'taskkill /IM {app_name} /F')
                return f"{app_name.capitalize()} kapatıldı."
            except Exception as e:
                return f"{app_name.capitalize()} kapatılamadı: {str(e)}"


        elif command.startswith("music:"):
            # Spotify'da şarkıyı çal
            song_name = command[6:].strip()
            spotify = SpotifyManager()
            return spotify.play_song(song_name)

        elif command.startswith("music_control:"):
            # Spotify müzik kontrolü (pause, resume, next, previous)
            action = command[14:].strip()
            spotify = SpotifyManager()
            if action == "pause":
                return spotify.pause_playback()
            elif action == "resume":
                return spotify.resume_playback()
            elif action == "next":
                return spotify.next_track()
            elif action == "previous":
                return spotify.previous_track()
            else:
                return "Geçersiz müzik kontrol komutu"

        else:
            return "Geçersiz komut formatı"

    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        return "Komut çalıştırılırken hata oluştu"
