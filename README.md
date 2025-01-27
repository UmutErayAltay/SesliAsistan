# Gemini AI Asistanı

Bu proje, Google Gemini API'sini kullanarak sesli komutları ve sohbet özelliklerini birleştiren basit bir yapay zeka asistanıdır. Özel kısayollar oluşturabilir ve yönetebilirsiniz.

## Özellikler

*   **Sesli Komutlar:** "Artemis" tetikleme kelimesiyle sesli komutları algılar ve işler.
*   **Sohbet Modu:** Gemini ile sohbet edebilirsiniz.
*   **Komut Modu:** Sistem komutlarını (cmd, web siteleri, kısayollar, uygulama kapatma) sesli olarak çalıştırabilirsiniz.
*   **Kısayol Yönetimi:** Özel uygulama ve dosya kısayolları oluşturabilir, düzenleyebilir ve silebilirsiniz.
*   **Kullanıcı Dostu Arayüz:** `customtkinter` ile oluşturulmuş basit ve kullanışlı bir grafik arayüzü.

## Gereksinimler

*   Python 3.x
*   Aşağıdaki Python kütüphaneleri (gereksinimler.txt dosyasında listelenmiştir)
*   Google Gemini API Anahtarı

## Kurulum

1.  **Depoyu klonlayın:**

    ```bash
    git clone [https://github.com/UmutErayAltay/SesliAsistan.git]
    cd [proje klasörünüz]
    ```

2.  **Gerekli kütüphaneleri yükleyin:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Google Gemini API Anahtarınızı ayarlayın:**
    *   [Google AI Studio](https://makersuite.google.com/app/apikey) adresinden bir API anahtarı alın.
    *   Proje dizininde `.env` adında bir dosya oluşturun.
    *   Aşağıdaki satırı `.env` dosyasına ekleyin ve `YOUR_API_KEY` yerine kendi API anahtarınızı yazın:

        ```
        GOOGLE_API_KEY=YOUR_API_KEY
        ```

## Kullanım

1.  **Uygulamayı çalıştırın:**

    ```bash
    python app.py
    ```

2.  **Arayüzü Kullanma:**
    *   Sol panelde kısayollarınızı yönetebilirsiniz. Yeni kısayollar ekleyebilir, düzenleyebilir ve silebilirsiniz.
    *   Sağ panelde sohbet veya komut modunu seçebilirsiniz.
    *   Mikrofon düğmesine tıklayarak sesli dinlemeyi başlatıp durdurabilirsiniz.
    *   Sesli komut vermek için "Artemis" kelimesiyle başlayın, ardından komutunuzu söyleyin (örneğin, "Artemis Google'ı aç").

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.


---

**Not:** Bu `README.md` dosyası bir örnektir. Projenize göre içeriği düzenleyebilirsiniz. Örneğin, daha detaylı kullanım talimatları, ekran görüntüleri veya ek özellikler ekleyebilirsiniz. 
