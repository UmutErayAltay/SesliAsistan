import pyttsx3
import speech_recognition as sr

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