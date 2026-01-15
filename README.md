# 📘 Program CYK Parsing Kalimat Bahasa Bali Berpredikat Frasa Adjektiva

## 📌 Tentang Aplikasi

**Program CYK Parsing Kalimat Bahasa Bali Berpredikat Frasa Adjektiva** adalah sebuah aplikasi berbasis Python yang dirancang untuk melakukan pengecekan dan analisis struktur grammar kalimat sederhana berpredikat frasa adjektiva dalam Bahasa Bali menggunakan **Context-Free Grammar (CFG)** dan **algoritma Cocke–Younger–Kasami (CYK)**.

---

## ✨ Fitur Utama

- 🔍 Parsing kalimat Bahasa Bali menggunakan algoritma CYK
- 📐 Implementasi Context-Free Grammar (CFG)
- 🧠 Validasi struktur kalimat berdasarkan aturan grammar
- 🌳 Visualisasi struktur parse tree (hierarki sintaksis)
- 🖥️ Antarmuka grafis (GUI) berbasis `CustomTkinter`
- 📊 Tabel CYK interaktif untuk analisis parsing

---

## ⚙️ Kemampuan dan Batasan Sistem

### ✅ Kemampuan

- Menganalisis kalimat sederhana Bahasa Bali
- Mendukung kalimat berpredikat **Frasa Adjektiva (AdjP)**
- Menampilkan hasil parsing dalam bentuk tabel dan struktur pohon

### ❌ Batasan

- Grammar masih terbatas pada aturan yang telah didefinisikan
- Belum mendukung kalimat kompleks atau majemuk
- Dataset kosakata masih bersifat terbatas dan statis
- Tidak mendukung analisis semantik atau morfologi lanjutan

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python 3.x
- **GUI Framework**: `tkinter` dan `customtkinter`

---

## 📂 Struktur Direktori Proyek

```
Program-CYK-Parsing-Kalimat-Bahasa-Bali/
│
├── main.py                   # Program utama untuk menjalankan parsing CYK
├── cyk-parser.py             # Implementasi algoritma CYK dan grammar CNF Bahasa Bali
├── cyk-parser-testing.py     # Pengujian parsing menggunakan dataset positif & negatif
├── dataset_positif.txt       # Dataset kalimat valid Bahasa Bali
├── dataset_negatif.txt       # Dataset kalimat tidak valid Bahasa Bali
├── requirements.txt          # Daftar dependensi Python
└── README.md                 # Dokumentasi proyek
```

### Penjelasan File dan Folder Penting

- **main.py**
  Berfungsi sebagai _entry point_ aplikasi. File ini menangani alur utama program, mulai dari membaca input kalimat, memanggil fungsi parsing CYK, hingga menampilkan hasil validasi grammar.

- **cyk-parser.py**
  Berisi implementasi utama algoritma **Cocke–Younger–Kasami (CYK)**. Pada file ini terdapat fungsi `get_bali_grammar()` yang mendefinisikan aturan **Context-Free Grammar (CFG)** Bahasa Bali dalam bentuk **Chomsky Normal Form (CNF)**, serta fungsi-fungsi pendukung untuk proses parsing.

- **cyk-parser-testing.py**
  Digunakan untuk melakukan pengujian sistem parsing secara otomatis menggunakan dataset kalimat valid dan tidak valid. File ini juga memiliki fungsi `get_bali_grammar()` sebagai sumber aturan grammar CNF yang sama dengan file utama, sehingga konsistensi grammar tetap terjaga saat evaluasi.

- **dataset_positif.txt**
  Berisi kumpulan kalimat Bahasa Bali yang **sesuai** dengan aturan grammar (kalimat valid). Dataset ini digunakan untuk menguji keberhasilan sistem dalam mengenali kalimat yang benar secara sintaksis.

- **dataset_negatif.txt**
  Berisi kumpulan kalimat Bahasa Bali yang **tidak sesuai** dengan aturan grammar (kalimat tidak valid). Dataset ini digunakan untuk menguji ketahanan sistem terhadap kesalahan struktur kalimat.

- **requirements.txt**
  Berisi daftar pustaka atau _library_ Python yang dibutuhkan agar program dapat dijalankan dengan baik.

---

## 🚀 Cara Instalasi dan Menjalankan Program

### 🔧 Prasyarat Sistem

- Python versi 3.8 atau lebih baru
- Sistem Operasi Windows / Linux / macOS

### 📥 Langkah-langkah Instalasi

1. **Clone repository**

   ```bash
   git clone https://github.com/Kusuma1403/Program-CYK-Parsing-Kalimat-Bahasa-Bali.git
   ```

2. **Masuk ke direktori proyek**

   ```bash
   cd Program-CYK-Parsing-Kalimat-Bahasa-Bali
   ```

3. **Instal dependensi**

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan program GUI**

   ```bash
   python gui_cyk.py
   ```

---

## ⚙️ Cara Kerja Aplikasi

1. Pengguna memasukkan kalimat Bahasa Bali melalui GUI
2. Kalimat dipecah menjadi token (kata)
3. Grammar CFG diterapkan untuk membentuk tabel CYK
4. Algoritma CYK mengevaluasi apakah kalimat valid
5. Jika valid, sistem membangun dan menampilkan parse tree

---

## 🧪 Contoh Penggunaan

**Input Kalimat (Predikat Harus di Awal Kalimat):**

```
Peteng dedet kamar i Putu
```

**Output:**

- Status: ✅ Kalimat valid
- Struktur sintaksis ditampilkan dalam tabel CYK
- Parse tree AdjP ditampilkan secara hierarkis

---

## 📘 Cara Penggunaan

1. Jalankan aplikasi
2. Masukkan kalimat Bahasa Bali pada kolom input
3. Klik tombol **Cek Kalimat**
4. Amati hasil analisis pada tabel triangular dan visualisasi parse tree
5. Klik **Reset** untuk mereset aplikasi ke keadaan awal

---

## 📚 Dataset & Kamus Kata

Dataset dan kamus kata pada aplikasi ini disusun secara **manual dan terkontrol** untuk mendukung proses parsing sintaksis menggunakan algoritma CYK.

### 📄 Dataset Kalimat

Dataset kalimat disimpan dalam dua berkas teks terpisah:

- **dataset_positif.txt**
  Berisi kumpulan kalimat sederhana Bahasa Bali yang **valid secara sintaksis** dan sesuai dengan aturan grammar yang telah didefinisikan, khususnya kalimat dengan **predikat Frasa Adjektiva (AdjP)**.

- **dataset_negatif.txt**
  Berisi kumpulan kalimat Bahasa Bali yang **tidak valid secara sintaksis**, baik karena urutan kata yang tidak sesuai, penggunaan kategori kata yang salah, maupun pelanggaran terhadap struktur grammar.

Dataset ini digunakan terutama pada proses **pengujian dan evaluasi** sistem melalui file `cyk-parser-testing.py` untuk mengukur kemampuan parser dalam membedakan kalimat yang benar dan salah.

### 📘 Kamus Kata dan Aturan Grammar

Kamus kata dan aturan grammar tidak disimpan dalam file terpisah, melainkan didefinisikan langsung dalam kode program melalui fungsi `get_bali_grammar()` yang terdapat pada:

- `cyk-parser.py`
- `cyk-parser-testing.py`

Aturan grammar disusun dalam bentuk **Context-Free Grammar (CFG)** yang telah dikonversi ke **Chomsky Normal Form (CNF)** agar kompatibel dengan algoritma CYK. Kamus kata mencakup pemetaan:

- **Terminal**: kata-kata Bahasa Bali (misalnya nomina dan adjektiva)
- **Non-terminal**: kategori sintaksis seperti S, NP, AdjP, Adj, dan simbol lainnya

Pendekatan ini memastikan bahwa setiap kalimat pada dataset dievaluasi secara konsisten berdasarkan aturan grammar formal yang sama.

---

## 🧾 Dataset Evaluasi

Dataset evaluasi berupa:

- Kalimat valid sesuai grammar
- Kalimat tidak valid sebagai pembanding

Evaluasi dilakukan secara kualitatif berdasarkan keberhasilan parsing.

---

## 🔮 Pengembangan Selanjutnya

Beberapa ide pengembangan lanjutan:

- 📈 Penambahan grammar kalimat kompleks
- 🌐 Dukungan kalimat predikat frasa lainnya, seperti frasa verba, preposisi, nomina, dan numeralia
- 🧩 Integrasi analisis morfologi Bahasa Bali
- 📊 Evaluasi otomatis akurasi parsing

---

## 📄 Lisensi

Proyek ini menggunakan lisensi **MIT License**.

Silakan gunakan, modifikasi, dan distribusikan proyek ini untuk keperluan akademik maupun pengembangan lebih lanjut dengan tetap mencantumkan atribusi kepada developer.

---

## 👨‍💻‍ Developer

**Kelompok 5A - Teori Bahasa dan Otomata**

Informatika 24 - FMIPA - Universitas Udayana

---
