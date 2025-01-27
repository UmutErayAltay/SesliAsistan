import customtkinter as ctk

from tkinter import messagebox, filedialog

import os

import shutil

from shortcuts_manager import SHORTCUTS_DIR, update_shortcuts_list

from ai_logic import create_chat_model, execute_command

from voice import listen

import threading

import speech_recognition as sr

from PIL import Image, ImageTk



class App(ctk.CTk):

    def __init__(self):

        super().__init__()



        # Font ayarları - __init__ içinde tanımlanmalı!

        self.baslik_font = ctk.CTkFont(family="Helvetica Neue", size=18, weight="bold")

        self.normal_font = ctk.CTkFont(family="Roboto", size=14)

        self.buton_font = ctk.CTkFont(family="Open Sans", size=14, weight="bold")



        # Renk paleti (daha koyu tonlar ve vurgu rengi)

        ana_renk = "#2C3E50"  # Koyu gri-mavi
        ikincil_renk = "#34495E" # Biraz daha açık gri-mavi
        vurgu_renk = "#1ABC9C"  # Turkuaz

        yazi_renk = "#ECF0F1"   # Açık gri



        # Tema ve görünüm ayarları

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("green") # Varsayılan temayı değiştirin, veya özel renkler kullanın



        # Ana pencere ayarları

        self.title("Gemini AI Asistan")

        self.geometry("1000x600")



        # Grid yapılandırması

        self.grid_rowconfigure(0, weight=1)  # Ana içerik

        self.grid_columnconfigure(0, weight=0)  # Sol panel

        self.grid_columnconfigure(1, weight=1)  # Sağ panel



        # Sol panel (Kısayollar)

        self.left_panel = ctk.CTkFrame(self, width=250, fg_color=ikincil_renk) # Arka plan rengi

        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.left_panel.grid_propagate(False)  # Genişliği sabitle



        # Kısayollar başlığı

        self.shortcuts_label = ctk.CTkLabel(

            self.left_panel,

            text="KISAYOLLAR",

            font=self.baslik_font, # self.baslik_font kullanıldı - DOĞRU YERDE!

            text_color=yazi_renk # Yazı rengi

        )

        self.shortcuts_label.pack(pady=10)



        # Kısayollar listesi

        self.shortcuts_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color=ikincil_renk) # Arka plan rengi

        self.shortcuts_frame.pack(fill="both", expand=True, padx=5, pady=5)



        # Kısayol ekle butonu

        self.add_shortcut_btn = ctk.CTkButton(

            self.left_panel,

            text="+ Kısayol Ekle",

            command=self.add_shortcut,

            font=self.buton_font, # self.buton_font kullanıldı - DOĞRU YERDE!

            fg_color=vurgu_renk, # Vurgu rengi

            hover_color="#16A085", # Daha koyu vurgu rengi

            text_color=yazi_renk

        )

        self.add_shortcut_btn.pack(pady=10, padx=10, fill="x")



        # Sağ panel

        self.right_panel = ctk.CTkFrame(self, fg_color=ana_renk) # Arka plan rengi

        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")



        # Mod değiştirme butonu

        self.mode = "chat"

        self.mode_btn = ctk.CTkButton(

            self.right_panel,

            text="MOD: SOHBET",

            command=self.toggle_mode,

            font=self.buton_font, # self.buton_font kullanıldı - DOĞRU YERDE!

            height=40,

            fg_color="#2FA572",  # Yeşil tonu

            hover_color="#248C61",  # Koyu yeşil

            text_color=yazi_renk

        )

        self.mode_btn.pack(pady=10, padx=10, fill="x")



        # Çıktı alanı

        self.output = ctk.CTkTextbox(

            self.right_panel,

            wrap="word",

            fg_color=ikincil_renk, # Arka plan rengi

            text_color=yazi_renk, # Yazı rengi

            font=self.normal_font # self.normal_font kullanıldı - DOĞRU YERDE!

        )

        self.output.pack(fill="both", expand=True, padx=10, pady=5)

        self.output.configure(state="disabled")  # Yazma ve düzenlemeyi engelle



        # Mikrofon çerçevesi

        self.mic_frame = ctk.CTkFrame(self.right_panel, fg_color=ana_renk) # Arka plan rengi

        self.mic_frame.pack(fill="x", padx=10, pady=5)



        # Mikrofon durumu etiketi

        self.mic_status = ctk.CTkLabel(

            self.mic_frame,

            text="🎤 Dinleme Kapalı",

            font=self.normal_font, # self.normal_font kullanıldı - DOĞRU YERDE!

            text_color=yazi_renk # Yazı rengi

        )

        self.mic_status.pack(side="left", padx=10)



        # Mikrofon butonu

        self.mic_btn = ctk.CTkButton(

            self.mic_frame,

            text="🎤",

            width=100,

            height=100,

            command=self.toggle_listening,

            fg_color=vurgu_renk,

            hover_color="#16A085",

            text_color=yazi_renk,

            corner_radius=50 # Yuvarlak buton için köşe yarıçapı

        )

        self.mic_btn.pack(side="right", padx=10, pady=10)



        # AI model ve bellek başlatma (ui.py içinde kalacak, veya app.py'ye taşınabilir)

        self.llm = create_chat_model()

        # Bellek yönetimi burada veya app.py'de olabilir. Şimdilik burada kalsın.

        from langchain.memory import ConversationBufferMemory

        self.memory = ConversationBufferMemory(return_messages=True)



        # Sistem şablonları (ai_logic.py'ye taşınabilir)

        from ai_logic import create_task_chain, create_chat_chain

        self.task_chain = create_task_chain(self.llm)

        self.chat_chain = create_chat_chain(self.llm)



        # Dinleme durumu

        self.is_listening = False

        self.listen_thread = None



        # Başlangıçta kısayolları yükle

        update_shortcuts_list(self) # self'i geçiriyoruz ki UI elemanlarına erişebilsin



    def toggle_mode(self):

        if self.mode == "chat":

            self.mode = "command"

            self.mode_btn.configure(

                text="MOD: KOMUT",

                fg_color="#E74C3C",  # Kırmızı tonu

                hover_color="#C0392B"  # Koyu kırmızı

            )

            self.update_output("\n--- Komut moduna geçildi ---\n")

        else:

            self.mode = "chat"

            self.mode_btn.configure(

                text="MOD: SOHBET",

                fg_color="#2FA572",  # Yeşil tonu

                hover_color="#248C61"  # Koyu yeşil

            )

            self.update_output("\n--- Sohbet moduna geçildi ---\n")



    def toggle_listening(self):

        if not self.is_listening:

            self.is_listening = True

            self.mic_btn.configure(fg_color="red")

            self.mic_status.configure(text="🎤 Dinleniyor...")

            self.listen_thread = threading.Thread(target=self.continuous_listen)

            self.listen_thread.daemon = True

            self.listen_thread.start()

        else:

            self.is_listening = False

            self.mic_btn.configure(fg_color=vurgu_renk)

            self.mic_status.configure(text="🎤 Dinleme Kapalı")



    def continuous_listen(self):

        r = sr.Recognizer()

        with sr.Microphone() as source:

            try:

                # Gürültü seviyesini ayarla

                r.adjust_for_ambient_noise(source, duration=1)

                # Ses algılama eşiğini ayarla

                r.energy_threshold = 400

                r.dynamic_energy_threshold = False

                while self.is_listening:

                    try:

                        self.mic_btn.configure(fg_color="green")  # Ses algılandığında yeşil yap

                        audio = r.listen(source, timeout=1, phrase_time_limit=10)

                        try:

                            text = r.recognize_google(audio, language='tr-TR')

                            # "Artemis" ile başlayan komutları kontrol et

                            if text.lower().startswith("artemis"):

                                command = text[8:].strip()  # "Artemis" kelimesinden sonrasını al

                                self.process_input(command)

                        except sr.UnknownValueError:

                            continue

                        except sr.RequestError:

                            self.update_output("Bağlantı hatası oluştu.")

                    except:

                        continue

                    finally:

                        self.mic_btn.configure(fg_color="red") # Dinleme bittiğinde kırmızı yap

            except Exception as e:

                self.update_output(f"Mikrofon başlatılırken hata oluştu: {str(e)}")



    def process_input(self, text):

        self.update_output(f"\nSiz: {text}")



        try:

            if self.mode == "command":

                response = self.task_chain.invoke({"input": text})

                command_result = execute_command(response.content)
                
                # Gemini'ye gönderilecek mesaja CMD çıktısını ekle
                gemini_input = f"{text}\n\nCMD Çıktısı:\n{command_result}"
                
                response = self.chat_chain.invoke({"input": gemini_input})
                self.update_output(f"Asistan: {response.content}")

            else:

                response = self.chat_chain.invoke({"input": text})

                self.update_output(f"Asistan: {response.content}")

        except Exception as e:

            self.update_output(f"Hata oluştu: {str(e)}")



    def update_output(self, text):

        self.output.configure(state="normal")  # Geçici olarak yazma izni ver

        self.output.insert("end", f"{text}\n")

        self.output.see("end")

        self.output.configure(state="disabled")  # Yazma iznini kaldır



    def update_shortcuts_list(self):

        """Kısayollar listesini güncelle"""

        # Önce mevcut widget'ları temizle

        for widget in self.shortcuts_frame.winfo_children():

            widget.destroy()



        # Kısayolları yükle

        from shortcuts_manager import shortcuts_dict # Import shortcuts_dict

        try:

            from pathlib import Path

            for file in Path(SHORTCUTS_DIR).glob('*.lnk'):

                if file.is_file():

                    shortcuts_dict[file.stem.lower()] = str(file)



                    shortcut_frame = ctk.CTkFrame(self.shortcuts_frame)

                    shortcut_frame.pack(fill="x", pady=2)



                    name_label = ctk.CTkLabel(shortcut_frame, text=file.stem)

                    name_label.pack(side="left", padx=5)



                    edit_btn = ctk.CTkButton(shortcut_frame, text="✏️", width=30,

                                           command=lambda n=file.stem: self.edit_shortcut(n))

                    edit_btn.pack(side="right", padx=2)



                    delete_btn = ctk.CTkButton(shortcut_frame, text="🗑️", width=30,

                                             command=lambda n=file.stem: self.delete_shortcut(n))

                    delete_btn.pack(side="right", padx=2)

        except Exception as e:

            messagebox.showerror("Hata", f"Kısayollar yüklenirken hata oluştu: {str(e)}")



    def add_shortcut(self):

        dialog = ctk.CTkInputDialog(text="Kısayol adını girin:", title="Kısayol Ekle")

        shortcut_name = dialog.get_input()

        if shortcut_name:

            file_path = filedialog.askopenfilename(

                title="Kısayol seçin",

                filetypes=[("Kısayollar", "*.lnk"), ("Tüm dosyalar", "*.*")]

            )

            if file_path:

                try:

                    target_path = os.path.join(SHORTCUTS_DIR, f"{shortcut_name}.lnk")

                    shutil.copy2(file_path, target_path)

                    from shortcuts_manager import update_shortcuts_list # Import update_shortcuts_list

                    update_shortcuts_list(self) # self'i geçiriyoruz

                except Exception as e:

                    messagebox.showerror("Hata", f"Kısayol eklenirken hata oluştu: {str(e)}")



    def edit_shortcut(self, name):

        dialog = ctk.CTkInputDialog(text="Yeni kısayol adını girin:", title="Kısayol Düzenle")

        new_name = dialog.get_input()

        if new_name:

            try:

                old_path = os.path.join(SHORTCUTS_DIR, f"{name}.lnk")

                new_path = os.path.join(SHORTCUTS_DIR, f"{new_name}.lnk")

                os.rename(old_path, new_path)

                from shortcuts_manager import update_shortcuts_list # Import update_shortcuts_list

                update_shortcuts_list(self) # self'i geçiriyoruz

            except Exception as e:

                messagebox.showerror("Hata", f"Kısayol düzenlenirken hata oluştu: {str(e)}")



    def delete_shortcut(self, name):

        if messagebox.askyesno("Kısayol Sil", f"{name} kısayolunu silmek istediğinize emin misiniz?"):

            try:

                os.remove(os.path.join(SHORTCUTS_DIR, f"{name}.lnk"))

                from shortcuts_manager import update_shortcuts_list # Import update_shortcuts_list

                update_shortcuts_list(self) # self'i geçiriyoruz

            except Exception as e:

                messagebox.showerror("Hata", f"Kısayol silinirken hata oluştu: {str(e)}") 