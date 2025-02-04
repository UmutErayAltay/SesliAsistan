import os

from dotenv import load_dotenv

from watchdog.observers import Observer

import time



# Özel modüller

from ui import App

from shortcuts_manager import ShortcutHandler, update_shortcuts, SHORTCUTS_DIR

from voice import setup_voice, speak, listen



# .env dosyasından API anahtarını yükle

load_dotenv()



if __name__ == "__main__":

    os.makedirs(SHORTCUTS_DIR, exist_ok=True)



    # Kısayol değişikliklerini izleyici

    event_handler = ShortcutHandler()

    observer = Observer()

    observer.schedule(event_handler, SHORTCUTS_DIR, recursive=False)

    observer.start()

    update_shortcuts() # Başlangıçta kısayolları yükle



    # Ses motorunu başlat

    engine = setup_voice()



    app = App() # UI uygulamasını başlat

    app.mainloop()



    observer.stop()

    observer.join() 