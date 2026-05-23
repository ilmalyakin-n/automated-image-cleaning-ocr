import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# ==============================================================================
# KONFIGURASI FOLDER
# ==============================================================================
FOLDER_RAW = "dataset_baru_raw"
# Folder baru untuk menampung duplikat agar data asli tidak terhapus permanen
FOLDER_DUPLIKAT_INTERNAL = os.path.join(FOLDER_RAW, "duplikat_internal")

THRESHOLD_PERBEDAAN = 4 
format_gambar = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')

os.makedirs(FOLDER_DUPLIKAT_INTERNAL, exist_ok=True)

# ==============================================================================
# PROSES: Deteksi Duplikat Sesama Data Raw
# ==============================================================================
print("=== TAHAP 1: Membersihkan Duplikat Internal di dataset_baru_raw ===")

unique_hashes = {}
jumlah_total = 0
jumlah_duplikat = 0

list_gambar = [f for f in os.listdir(FOLDER_RAW) if f.lower().endswith(format_gambar)]

for filename in tqdm(list_gambar, desc="Memindai Data Raw"):
    path_gambar = os.path.join(FOLDER_RAW, filename)
    jumlah_total += 1
    
    try:
        with Image.open(path_gambar) as img:
            img_hash = imagehash.phash(img)
        
        # Cek apakah hash mirip dengan gambar yang sudah dipindai sebelumnya
        is_duplicate = False
        for saved_hash in unique_hashes.keys():
            if (img_hash - saved_hash) <= THRESHOLD_PERBEDAAN:
                is_duplicate = True
                break
        
        if not is_duplicate:
            # Jika unik, catat hash-nya
            unique_hashes[img_hash] = filename
        else:
            # Jika duplikat, pindahkan ke folder duplikat_internal
            shutil.move(path_gambar, os.path.join(FOLDER_DUPLIKAT_INTERNAL, filename))
            jumlah_duplikat += 1
            
    except Exception as e:
        print(f"Gagal memproses {filename}: {e}")

print("\n" + "="*40)
print("=== SELESAI MEMBERSIHKAN DATA RAW ===")
print("="*40)
print(f"Total gambar diperiksa         : {jumlah_total} gambar")
print(f"Gambar UNIK (Tetap di folder)  : {jumlah_total - jumlah_duplikat} gambar")
print(f"Gambar DUPLIKAT (Dipindahkan)  : {jumlah_duplikat} gambar")
print(f"Lokasi gambar duplikat         : {FOLDER_DUPLIKAT_INTERNAL}")
print("="*40)
print("Silakan lanjut menjalankan 'clean.py' untuk tahap berikutnya.")