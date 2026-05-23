import os
import subprocess
import sys

def run_script(script_name):
    print(f"\n[PIPELINE] Menjalankan: {script_name}...")
    if not os.path.exists(script_name):
        print(f"[ERROR] File {script_name} tidak ditemukan di folder saat ini!")
        return False
    
    # Menjalankan script python terpisah
    result = subprocess.run([sys.executable, script_name])
    
    if result.returncode == 0:
        print(f"[SUCCESS] {script_name} berhasil diselesaikan.")
        return True
    else:
        print(f"[FAILED] Terjadi kesalahan saat menjalankan {script_name}.")
        return False

if __name__ == "__main__":
    print("="*50)
    print("STARTING DATA CLEANING PIPELINE FOR NUTRITION OCR")
    print("="*50)
    
    # Urutan eksekusi pipeline yang logis
    pipeline_steps = [
        "clean_internal_raw.py",  # 1. Bersihkan duplikat sesama data baru
        "clean.py",               # 2. Bersihkan duplikat terhadap data lama
        "filter_quality.py",      # 3. Buang gambar buram / kekecilan
        "rename.py"               # 4. Rapikan nama file (hapus spasi)
    ]
    
    success = True
    for step in pipeline_steps:
        if not run_script(step):
            print("\n[PIPELINE ABORTED] Proses dihentikan karena terjadi error.")
            success = False
            break
            
    if success:
        print("\n" + "="*50)
        print("PIPELINE SELESAI: Data Anda 100% Premium & Siap Di-anotasi!")
        print("="*50)