# =======================================================================================
# Deskripsi: Berisi logika untuk pengujian kalimat bahasa Bali dari dataset_positif.txt
#            dan dataset_negatif.txt menggunakan Algoritma CYK (Cocke-Kasami-Younger)
# =======================================================================================

from cyk_parser import get_bali_grammar, cyk_parse

###

def run_full_evaluation(positive_sentences, negative_sentences, grammar):
    """
    Fungsi untuk menjalankan skenario evaluasi lengkap dengan Confusion Matrix.
    """
    import time

    # Inisialisasi Counter
    TP = 0  # True Positive (Data Positif, Terdeteksi Valid)
    FN = 0  # False Negative (Data Positif, Terdeteksi Invalid/Salah)
    TN = 0  # True Negative (Data Negatif, Terdeteksi Invalid)
    FP = 0  # False Positive (Data Negatif, Terdeteksi Valid/Salah)

    print("\n" + "="*105)
    print(f"| {'NO':<4} | {'KALIMAT INPUT':<45} | {'JENIS DATA':<12} | {'PREDIKSI':<10} | {'HASIL':<15} |")
    print("="*105)

    counter = 1
    
    # --- TAHAP 1: PENGUJIAN DATA POSITIF (Harapannya VALID) ---
    for kalimat in positive_sentences:
        kalimat_bersih = kalimat.strip().lower()
        
        # Jalankan CYK
        is_valid, _, tokens_baru = cyk_parse(kalimat_bersih, grammar)
        kalimat_display = ' '.join(tokens_baru)

        if is_valid:
            prediksi = "VALID"
            hasil_evaluasi = "BENAR (TP)"
            TP += 1
        else:
            prediksi = "INVALID"
            hasil_evaluasi = "SALAH (FN)"
            FN += 1
        
        print(f"| {counter:<4} | {kalimat_display:<45} | {'POSITIF':<12} | {prediksi:<10} | {hasil_evaluasi:<15} |")
        counter += 1

    # --- TAHAP 2: PENGUJIAN DATA NEGATIF (Harapannya INVALID) ---
    for kalimat in negative_sentences:
        kalimat_bersih = kalimat.strip().lower()
        
        # Jalankan CYK
        is_valid, _, tokens_baru = cyk_parse(kalimat_bersih, grammar)
        kalimat_display = ' '.join(tokens_baru)

        if not is_valid:  # Jika sistem menolak, itu bagus!
            prediksi = "INVALID"
            hasil_evaluasi = "BENAR (TN)"
            TN += 1
        else:             # Jika sistem menerima, itu salah!
            prediksi = "VALID"
            hasil_evaluasi = "SALAH (FP)"
            FP += 1
            
        print(f"| {counter:<4} | {kalimat_display:<45} | {'NEGATIF':<12} | {prediksi:<10} | {hasil_evaluasi:<15} |")
        counter += 1

    # --- HITUNG AKURASI & TAMPILKAN LAPORAN ---
    total_data = TP + FN + TN + FP
    if total_data > 0:
        akurasi = ((TP + TN) / total_data) * 100
    else:
        akurasi = 0

    print("="*105)
    print("\n" + "="*40)
    print("      LAPORAN EVALUASI MODEL")
    print("="*40)
    print(f"Total Data Uji      : {total_data} Kalimat")
    print("-" * 40)
    print(f"1. True Positive (TP)  : {TP:<3} (Positif -> Valid)")
    print(f"2. False Negative (FN) : {FN:<3} (Positif -> Invalid)")
    print(f"3. True Negative (TN)  : {TN:<3} (Negatif -> Invalid)")
    print(f"4. False Positive (FP) : {FP:<3} (Negatif -> Valid)")
    print("-" * 40)
    print(f"TINGKAT AKURASI        : {akurasi:.2f}%")
    print("="*40)

###
# ==========================================
# BLOK UTAMA (MAIN) UNTUK PENGUJIAN LANGSUNG
# ==========================================
if __name__ == "__main__":
    # 1. Memuat Grammar
    my_grammar = get_bali_grammar()
    
    # Nama File
    file_positif = 'dataset_positif.txt' # Ubah nama file Anda yang berisi 50 kalimat disini
    file_negatif = 'dataset_negatif.txt' # Buat file baru berisi 20 kalimat salah

    # List Penampung
    data_positif = []
    data_negatif = []

    print("Sedang memuat dataset...")

    # 2. Membaca File Positif
    try:
        with open(file_positif, 'r') as f:
            data_positif = [line.strip() for line in f if line.strip()]
        print(f"[OK] Berhasil memuat {len(data_positif)} kalimat positif.")
    except FileNotFoundError:
        print(f"[ERROR] File '{file_positif}' tidak ditemukan!")

    # 3. Membaca File Negatif
    try:
        with open(file_negatif, 'r') as f:
            data_negatif = [line.strip() for line in f if line.strip()]
        print(f"[OK] Berhasil memuat {len(data_negatif)} kalimat negatif.")
    except FileNotFoundError:
        print(f"[WARNING] File '{file_negatif}' tidak ditemukan! Pengujian hanya berjalan parsial.")

    # 4. Jalankan Evaluasi
    if data_positif or data_negatif:
        run_full_evaluation(data_positif, data_negatif, my_grammar)
    else:
        print("Tidak ada data untuk diuji.")
