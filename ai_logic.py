from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()

def create_chat_model():
    """Gemini modelini başlatır"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    return llm

def create_task_chain(llm):
    """Görev zincirini oluşturur"""
    task_prompt = ChatPromptTemplate.from_messages([
        ("system", """Sen bir görev analiz asistanısın. Kullanıcının isteklerini analiz edip uygun komutu üretmelisin.
        Yanıtını şu formatlardan biriyle vermelisin:
        - cmd:komut -> Windows komut satırı komutu
        - web:adres -> Web sitesi açma
        - shortcut:isim -> Kısayol açma
        - close:uygulama_adı -> Uygulamayı kapatma"""), # close komutu eklendi
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
    import subprocess
    import webbrowser
    from shortcuts_manager import shortcuts_dict
    import os

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
            if app_name in shortcuts_dict:
                # Kapatmak için uygulamanın adını bul
                try:
                    # Uygulama kapatma komutu
                    os.system(f'taskkill /IM {app_name}.exe /F')
                    return f"{app_name.capitalize()} kapatıldı."
                except Exception as e:
                    return f"{app_name.capitalize()} kapatılamadı: {str(e)}"
            else:
                return f"Kapatılacak uygulama bulunamadı: {app_name}"

        else:
            return "Geçersiz komut formatı"

    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        return "Komut çalıştırılırken hata oluştu" 