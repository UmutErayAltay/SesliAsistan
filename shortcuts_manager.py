import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from pathlib import Path
import customtkinter as ctk
import tkinter.messagebox as messagebox

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

def update_shortcuts_list(app):
    """Kısayollar listesini UI üzerinde günceller"""
    if app is None or not hasattr(app, 'shortcuts_frame'):
        print("Hata: 'app' örneği veya 'shortcuts_frame' özelliği bulunamadı.")
        return

    # Önce mevcut widget'ları temizle
    for widget in app.shortcuts_frame.winfo_children():
        widget.destroy()

    # Kısayolları yükle
    try:
        for file in Path(SHORTCUTS_DIR).glob('*.lnk'):
            if file.is_file():
                shortcuts_dict[file.stem.lower()] = str(file)

                shortcut_frame = ctk.CTkFrame(app.shortcuts_frame)
                shortcut_frame.pack(fill="x", pady=2)

                name_label = ctk.CTkLabel(shortcut_frame, text=file.stem)
                name_label.pack(side="left", padx=5)

                edit_btn = ctk.CTkButton(shortcut_frame, text="✏️", width=30,
                                       command=lambda n=file.stem: app.edit_shortcut(n))
                edit_btn.pack(side="right", padx=2)

                delete_btn = ctk.CTkButton(shortcut_frame, text="🗑️", width=30,
                                         command=lambda n=file.stem: app.delete_shortcut(n))
                delete_btn.pack(side="right", padx=2)
    except Exception as e:
        messagebox.showerror("Hata", f"Kısayollar yüklenirken hata oluştu: {str(e)}") 