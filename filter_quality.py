import os
import shutil
from PIL import Image
from tqdm import tqdm

# ==============================================================================
# KONFIGURASI THRESHOLD (Standar Kualitas TINGGI / Premium OCR)
# ==============================================================================
FOLDER_TARGET = "dataset_baru_bersih"
FOLDER_TERBUANG = os.path.join(FOLDER_TARGET, "terlalu_kecil")

# Angka ini dinaikkan secara signifikan agar hanya gambar SANGAT JELAS yang lolos
MIN_WIDTH = 640       # Resolusi standar input training YOLOv8 (agak besar)
MIN_HEIGHT = 640      # Mencegah teks hancur/pecah saat di-resize oleh model
MIN_FILE_SIZE_KB = 80 # Membuang gambar hasil kompresi parah (buram/pixelated)

format_gambar = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
os.makedirs(FOLDER_TERBUANG, exist_ok=True)

# ==============================================================================
# PROSES FILTERING STRICT
# ==============================================================================
print("=== TAHAP 3: Memfilter Gambar Kualitas PREMIUM ===")

list_gambar = [f for f in os.listdir(FOLDER_TARGET) if f.lower().endswith(format_gambar)]
lolos = 0
terbuang = 0

for filename in tqdm(list_gambar, desc="Menyeleksi Ketajaman"):
    path_gambar = os.path.join(FOLDER_TARGET, filename)
    
    try:
        # 1. Cek ukuran file fisik (KB)
        file_size_kb = os.path.getsize(path_gambar) / 1024
        
        # 2. Cek dimensi piksel (Width x Height)
        with Image.open(path_gambar) as img:
            width, height = img.size
            
        # Kondisi: Jika SALAH SATU saja di bawah standar premium, langsung buang!
        if width < MIN_WIDTH or height < MIN_HEIGHT or file_size_kb < MIN_FILE_SIZE_KB:
            shutil.move(path_gambar, os.path.join(FOLDER_TERBUANG, filename))
            terbuang += 1
        else:
            lolos += 1
            
    except Exception as e:
        print(f"Gagal memproses {filename}: {e}")

# ==============================================================================
# HASIL AKHIR
# ==============================================================================
print("\n" + "="*45)
print("=== PROSES FILTER KUALITAS PREMIUM SELESAI ===")
print("="*45)
print(f"Gambar SUPER JELAS (Siap Anotasi)  : {lolos} gambar")
print(f"Gambar BURAM/KECIL (Dibuang)       : {terbuang} gambar")
print(f"Lokasi gambar buangan              : {FOLDER_TERBUANG}")
print("="*45)
print("Sekarang dataset Anda sudah berstandar tinggi. Silakan lanjut 'rename.py'!")