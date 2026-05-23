import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# ==============================================================================
# KONFIGURASI FOLDER (Sudah disesuaikan dengan screenshot data_ocr Anda)
# ==============================================================================
# Menggunakan relative path karena clean.py berada di folder yang sama
FOLDER_LAMA = "data_lama"
FOLDER_BARU_RAW = "dataset_baru_raw"
FOLDER_BARU_BERSIH = "dataset_baru_bersih"

# Batas toleransi perbedaan sidik jari gambar (0-4 sangat mirip/hampir identik)
THRESHOLD_PERBEDAAN = 4 

# Pastikan folder tujuan bersih sudah dibuat
os.makedirs(FOLDER_BARU_BERSIH, exist_ok=True)

# ==============================================================================
# PROSES 1: Menganalisis Gambar Lama Anda (84 Gambar)
# ==============================================================================
hash_gambar_lama = set()
format_gambar = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')

print("Step 1: Menganalisis sidik jari visual dari data_lama...")
if not os.path.exists(FOLDER_LAMA):
    print(f"Error: Folder '{FOLDER_LAMA}' tidak ditemukan!")
    exit()

for filename in os.listdir(FOLDER_LAMA):
    if filename.lower().endswith(format_gambar):
        path = os.path.join(FOLDER_LAMA, filename)
        try:
            with Image.open(path) as img:
                # Menggunakan pHash untuk mendeteksi kesamaan struktur tabel gizi
                img_hash = imagehash.phash(img)
                hash_gambar_lama.add(img_hash)
        except Exception as e:
            print(f"Gagal memproses gambar lama {filename}: {e}")

print(f"Berhasil merekam {len(hash_gambar_lama)} gambar acuan dari data_lama.\n")

# ==============================================================================
# PROSES 2: Memfilter Gambar Baru dari Repositori Luar
# ==============================================================================
print("Step 2: Memfilter gambar di dataset_baru_raw...")
if not os.path.exists(FOLDER_BARU_RAW):
    print(f"Error: Folder '{FOLDER_BARU_RAW}' tidak ditemukan!")
    exit()

jumlah_lolos = 0
jumlah_duplikat_dibuang = 0

list_gambar_baru = [f for f in os.listdir(FOLDER_BARU_RAW) if f.lower().endswith(format_gambar)]

for filename in tqdm(list_gambar_baru, desc="Memproses"):
    path_baru = os.path.join(FOLDER_BARU_RAW, filename)
    try:
        with Image.open(path_baru) as img:
            hash_baru = imagehash.phash(img)
        
        # Cek apakah kemiripannya di bawah threshold
        is_duplicate = False
        for hash_lama in hash_gambar_lama:
            if (hash_baru - hash_lama) <= THRESHOLD_PERBEDAAN:
                is_duplicate = True
                break
        
        # Jika benar-benar baru, copy ke folder dataset_baru_bersih
        if not is_duplicate:
            shutil.copy(path_baru, os.path.join(FOLDER_BARU_BERSIH, filename))
            jumlah_lolos += 1
        else:
            jumlah_duplikat_dibuang += 1
            
    except Exception as e:
        print(f"Gagal memproses gambar baru {filename}: {e}")

# ==============================================================================
# HASIL AKHIR
# ==============================================================================
print("\n" + "="*40)
print("=== PROSES FILTER DUPLIKAT SELESAI ===")
print("="*40)
print(f"Gambar BARU & UNIK (Disimpan di dataset_baru_bersih) : {jumlah_lolos} gambar")
print(f"Gambar DUPLIKAT dengan data lama (Dibuang otomatis)   : {jumlah_duplikat_dibuang} gambar")
print("="*40)