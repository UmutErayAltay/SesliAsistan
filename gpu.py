import torch
import time

# GPU'yu kullanabilir miyiz kontrol et
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Kullanılan cihaz: {device}")

# Rastgele iki büyük tensor oluştur
size = 10000  # 1000x1000 boyutunda
x = torch.rand(size, size, device=device)
y = torch.rand(size, size, device=device)

# GPU'da matris çarpma işlemi yap
print("GPU üzerinde işlem başlıyor...")
start_time = time.time()
result = torch.matmul(x, y)
end_time = time.time()

print(f"İşlem tamamlandı! Süre: {end_time - start_time:.4f} saniye")
print(f"Sonuç tensorunun cihazı: {result.device}")  # GPU'da mı kontrol et
