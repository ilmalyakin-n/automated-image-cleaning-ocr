import os

FOLDER_BERSIH = "dataset_baru_bersih"
format_gambar = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')

print("=== TAHAP 4: Merapikan Nama File Dataset Premium ===")

if not os.path.exists(FOLDER_BERSIH):
    print(f"Error: Folder '{FOLDER_BERSIH}' tidak ditemukan!")
    exit()

# Mengambil hanya file gambar (otomatis mengabaikan folder 'terlalu_kecil')
list_gambar = [f for f in os.listdir(FOLDER_BERSIH) if f.lower().endswith(format_gambar)]
list_gambar.sort()

print(f"Mulai mengubah nama {len(list_gambar)} gambar...")

for index, filename in enumerate(list_gambar, start=1):
    ext = os.path.splitext(filename)[1].lower()
    
    # Format nama baru yang aman tanpa spasi: gizi_0001, gizi_0002, dst.
    nama_baru = f"gizi_{index:04d}{ext}"
    
    path_lama = os.path.join(FOLDER_BERSIH, filename)
    path_baru = os.path.join(FOLDER_BERSIH, nama_baru)
    
    try:
        os.rename(path_lama, path_baru)
    except Exception as e:
        print(f"Gagal mengubah nama {filename}: {e}")

print(f"Selesai! {len(list_gambar)} gambar kini berurutan dari gizi_0001 sampai gizi_{len(list_gambar):04d}!")