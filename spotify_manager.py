# spotify_manager.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

class SpotifyManager:
    def __init__(self):
        load_dotenv()
        
        # Spotify API kimlik bilgileri
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # Yeni redirect URI ve cache path
        self.redirect_uri = "http://127.0.0.1:9090"
        cache_path = ".spotify_cache"
        
        # Spotify istemcisini başlat
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-read-playback-state user-modify-playback-state user-read-currently-playing",
            cache_path=cache_path,
            open_browser=True
        ))
    
    def play_song(self, query):
        """Şarkı ara ve çal"""
        try:
            # Şarkıyı ara
            results = self.sp.search(q=query, limit=1, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                self.sp.start_playback(uris=[track_uri])
                track_name = results['tracks']['items'][0]['name']
                artist_name = results['tracks']['items'][0]['artists'][0]['name']
                return f"'{track_name}' - {artist_name} çalınıyor"
            return "Şarkı bulunamadı"
        except Exception as e:
            return f"Şarkı çalınırken hata oluştu: {str(e)}"
    
    def next_track(self):
        """Sonraki şarkıya geç"""
        try:
            self.sp.next_track()
            return "Sonraki şarkıya geçildi"
        except Exception as e:
            return f"Şarkı değiştirirken hata oluştu: {str(e)}"
    
    def previous_track(self):
        """Önceki şarkıya geç"""
        try:
            self.sp.previous_track()
            return "Önceki şarkıya geçildi"
        except Exception as e:
            return f"Şarkı değiştirirken hata oluştu: {str(e)}"
    
    def pause_playback(self):
        """Çalmayı duraklat"""
        try:
            self.sp.pause_playback()
            return "Müzik duraklatıldı"
        except Exception as e:
            return f"Müzik duraklatılırken hata oluştu: {str(e)}"
    
    def resume_playback(self):
        """Çalmaya devam et"""
        try:
            self.sp.start_playback()
            return "Müzik devam ediyor"
        except Exception as e:
            return f"Müzik başlatılırken hata oluştu: {str(e)}"
    
    def get_current_track(self):
        """Şu an çalan şarkıyı getir"""
        try:
            current = self.sp.current_playback()
            if current and current['item']:
                track_name = current['item']['name']
                artist_name = current['item']['artists'][0]['name']
                return f"Şu an çalıyor: {track_name} - {artist_name}"
            return "Şu an çalan şarkı yok"
        except Exception as e:
            return f"Şarkı bilgisi alınırken hata oluştu: {str(e)}"