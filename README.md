# Automated Data Cleaning Pipeline for Nutrition Label OCR

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Roboflow](https://img.shields.io/badge/Roboflow-CLI_Integration-purple.svg)](https://roboflow.com/)
[![Project Stage](https://img.shields.io/badge/Capstone_Project-Diabetes_Coding_Camp_2026-orange.svg)]()

Repository ini berisi sistem otomatisasi pembersihan data gambar (*Data Cleaning Pipeline*) untuk proyek deteksi objek dan OCR pada tabel informasi nilai gizi produk. Proyek ini dikembangkan sebagai bagian dari **Capstone Project - Diabetes Coding Camp 2026**.

Sistem ini dibangun untuk mengatasi masalah klasik dalam pengumpulan dataset berbasis visi komputer (*Computer Vision*): penamaan file yang berantakan, adanya data duplikat, serta gambar beresolusi rendah (buram) yang dapat menurunkan performa akurasi model (YOLOv8).

---

## 📌 Latar Belakang & Masalah

Dalam proyek OCR Informasi Gizi, akurasi pembacaan teks sangat dipengaruhi oleh kualitas piksel gambar. Dataset awal yang kami peroleh dari repositori publik dan kontribusi tim memiliki beberapa kendala:

1. **Duplikasi Data:** Terdapat banyak gambar yang sama persis namun memiliki nama file berbeda.
2. **Potensi Kebocoran Data (*Data Leakage*):** Ada irisan gambar baru yang kembar dengan data validasi/uji lama kami.
3. **Kualitas Rendah:** Banyak gambar hasil kompresi tinggi (di bawah standar YOLOv8 640×640 piksel) yang teks tabel gizinya tidak terbaca jelas.
4. **Format Nama Berantakan:** Karakter spasi bawaan platform pesan (seperti WhatsApp) sering memicu *syntax error* saat proses *training* di server Linux/Cloud.

Sesuai prinsip **"Garbage In, Garbage Out"**, pipeline ini dirancang untuk menyaring hanya data premium (Super Jelas & Unik) sebelum diunggah ke platform anotasi Roboflow.

---

## 🛠️ Langkah Kerja & Arsitektur Pipeline

Sistem pembersihan data dibagi menjadi 4 tahap logis yang dijalankan berurutan:

### 1. Pembersihan Duplikat Internal (`clean_internal_raw.py`)

Menggunakan algoritma *Perceptual Hashing (pHash)* melalui *library* `ImageHash` untuk memindai sidik jari visual gambar di dalam folder `dataset_baru_raw`. Gambar yang kembar sesama data baru akan dipisahkan secara otomatis.

### 2. Pencegahan Kebocoran Data Cross-Dataset (`clean.py`)

Membandingkan sidik jari visual seluruh data baru dengan 84 gambar acuan utama dari data lama (`data_lama`). Jika ada data baru yang terdeteksi mirip, sistem akan membuangnya demi menjaga objektivitas pengujian model (*Anti-Data Leakage*).

### 3. Penyaringan Kualitas Ketat (`filter_quality.py`)

Menerapkan ambang batas (*threshold*) kualitas tinggi untuk keperluan OCR:

- **Resolusi Minimum:** 640×640 piksel (menyesuaikan standar input YOLOv8).
- **Ukuran File Minimum:** 80 KB (menyingkirkan kompresi ekstrem).

Gambar di bawah standar dipisahkan ke folder khusus agar tidak membuang waktu tim saat proses anotasi tabel gizi (*calories, carbs, fat, sugar, sodium*).

### 4. Standardisasi & Sanitisasi Nama File (`rename.py`)

Mengubah nama seluruh file gambar premium yang tersisa menjadi terurut (`gizi_0001.jpg` s.d selesai) sekaligus memusnahkan karakter spasi dan simbol aneh yang berpotensi merusak jalannya skrip *training*.

### 🚀 Eksekusi Otomatis Sekali Klik (`run_pipeline.py`)

Bertindak sebagai manajer utama (*orchestrator*) yang mengeksekusi ke-4 skrip di atas secara berurutan dalam satu perintah terminal.

---

## 📂 Struktur Repositori

```text
data_ocr/
│
├── data_lama/                      # 158 Gambar acuan utama proyek lama
├── dataset_baru_raw/               # Tempat menaruh dataset mentah hasil unduhan
│   └── duplikat_internal/          # [Auto-Generated] Tempat gambar duplikat internal
│
├── dataset_baru_bersih/            # [Auto-Generated] Hasil akhir dataset PREMIUM
│   └── terlalu_kecil/              # [Auto-Generated] Gambar buram/kecil yang terbuang
│
├── clean_internal_raw.py           # Tahap 1: Deteksi kembaran di data baru
├── clean.py                        # Tahap 2: Filter duplikat terhadap data lama
├── filter_quality.py               # Tahap 3: Filter ketajaman piksel & resolusi
├── rename.py                       # Tahap 4: Penataan nomor file & hapus spasi
└── run_pipeline.py                 # File utama pengeksekusi seluruh pipeline
```

---

## 📊 Hasil Pembersihan Dataset (*Cleaning Metrics*)

Melalui eksekusi pipeline otomatis ini, berikut metrik efisiensi pengondisian data yang kami capai:

| Kategori Data / Filter | Jumlah Gambar | Keterangan Status |
|---|---|---|
| **Dataset Mentah Awal** | 1518 gambar | Dataset mentah belum disortir |
| **Filter Duplikat Internal** | -11 gambar | Dibuang karena kembar internal |
| **Filter Duplikat Data Lama** | -81 gambar | Dibuang demi mencegah *Data Leakage* |
| **Filter Kualitas Rendah** | -21 gambar | Dibuang karena resolusi < 640px / file < 80KB |
| **Dataset Premium Akhir** | **1395 gambar** | **Lolos Seleksi & Siap Di-anotasi** |

---

## 💾 Catatan Penting Mengenai Dataset

> ⚠️ **PEMBERITAHUAN UKURAN FILE:**
> Dikarenakan adanya aturan batas ukuran berkas (*file size limit*) dari GitHub untuk repositori standar, folder kumpulan data fisiknya (`data_lama/`, `dataset_baru_raw/`, dan `dataset_baru_bersih/`) **TIDAK dimasukkan** ke dalam *source tree* utama repositori ini.
>
> Seluruh arsip dataset mentah maupun dataset premium siap pakai telah kami unggah dan amankan pada menu **[GitHub Releases](https://github.com/username/repository/releases)** di repositori ini. Silakan unduh berkas zip dari sana dan ekstrak ke dalam direktori root proyek ini jika Anda ingin melakukan replikasi pengujian pipeline.

---

## 💻 Cara Menjalankan Pipeline Lokal

### 1. Instalasi Library Dependensi

Pastikan Anda sudah menginstal pustaka Python yang diperlukan:

```bash
pip install Pillow imagehash tqdm roboflow
```

### 2. Menjalankan Seluruh Pipeline

Cukup jalankan satu perintah utama ini di terminal Anda untuk memproses pembersihan data secara *end-to-end*:

```bash
python run_pipeline.py
```

### 3. Otomatisasi Unggah ke Roboflow (CLI Mode)

Setelah pipeline selesai, gunakan Roboflow CLI untuk mengunggah dataset premium langsung ke ruang kerja tim tanpa melalui browser:

```bash
roboflow login
roboflow import -p nutrition_label dataset_baru_bersih
```

---

## 👥 Kontributor

**Tim Data Science - Diabetes Coding Camp 2026**

- Ilmal Yakin N
- Diah Putri Kartikasari
