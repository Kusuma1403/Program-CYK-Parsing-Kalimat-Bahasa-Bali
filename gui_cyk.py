# ==============================================================================
# Deskripsi: Antarmuka Grafis (GUI) untuk aplikasi Parser Bahasa Bali.
#            Menggunakan Tkinter untuk input pengguna dan visualisasi tabel.
# ==============================================================================

import tkinter as tk
from tkinter import scrolledtext, messagebox
# Mengimpor fungsi logika dari file Program_CYK_Table.py
from Program_CYK_Table import get_bali_grammar, cyk_parse, get_cyk_table_string

def proses_gui():
    """
    Fungsi callback yang dipanggil saat tombol 'CEK KALIMAT' ditekan.
    Mengambil input, menjalankan parser, dan memperbarui GUI.
    """

    # Ambil teks dari input field
    kalimat_input = entry_kalimat.get()
    
    # Validasi input kosong
    if not kalimat_input.strip():
        messagebox.showwarning("Peringatan", "Mohon masukkan kalimat!")
        return

    # Preprocessing sederhana untuk tampilan
    kalimat_bersih = kalimat_input.strip().lower()
    
    # PANGGIL ALGORITMA CYK DI SINI
    # my_grammar diambil dari variabel global yang diinisialisasi di bawah
    is_valid, table_hasil, tokens_baru = cyk_parse(kalimat_bersih, my_grammar)
    
    # Panggil fungsi untuk menggambar hasil di Canvas
    gambar_piramida(canvas_output, table_hasil, tokens_baru)
    
    # Perbarui Label Status (Valid/Invalid)
    if is_valid:
        lbl_status.config(text="STATUS: VALID (DITERIMA)", fg="green")
    else:
        lbl_status.config(text="STATUS: INVALID (DITOLAK)", fg="red")

def gambar_piramida(canvas, table, tokens):
    """
    Fungsi visualisasi inti. Menggambar tabel segitiga CYK pada Canvas Tkinter.
    Menggunakan logika 'Lebar Dinamis' agar kotak menyesuaikan panjang teks.
    """
    # Bersihkan canvas dari gambar sebelumnya
    canvas.delete("all") 
    
    n = len(tokens)
    if n == 0: return

    # --- KONFIGURASI GAMBAR ---
    BOX_HEIGHT = 50       # Tinggi setiap kotak (pixel)
    START_X = 50          # Margin kiri awal
    BASE_Y = 50 + (n * BOX_HEIGHT) # Posisi Y dasar (baris paling bawah)
    
    COLOR_BOX = "#FFE4C4" # Warna isi kotak (Bisque)
    COLOR_TEXT = "black"  # Warna teks

    # ======================================================
    # LANGKAH 1: PRE-CALCULATION (Hitung Lebar Kolom)
    # Kita tidak bisa menggunakan lebar tetap karena teks isi sel bisa panjang.
    # ======================================================
    col_widths = [] # List untuk menyimpan lebar pixel setiap kolom

    for i in range(n):
        # Mulai dengan panjang kata token itu sendiri
        max_char_len = len(tokens[i]) 
        
        # Cek isi semua sel di atas token ini (secara vertikal di tabel segitiga)
        for length in range(1, n - i + 1):
            j = i + length - 1
            if table[i][j]:
                # Gabungkan isi sel menjadi string (misal: "NP, S, Pel")
                isi = ", ".join(sorted(list(table[i][j])))
                # Update panjang maksimum jika isi sel ini lebih panjang
                max_char_len = max(max_char_len, len(isi))
        
        # Rumus Lebar: (Jumlah Karakter * 9 pixel estimasi font) + Padding 20px
        # Minimal lebar 100px agar kotak tidak terlalu gepeng
        calculated_width = max(100, (max_char_len * 9) + 20)
        col_widths.append(calculated_width)

    # Update area scroll canvas agar seluruh gambar bisa di-scroll
    total_width = sum(col_widths) + 100
    total_height = (n * BOX_HEIGHT) + 150
    canvas.config(scrollregion=(0, 0, total_width, total_height))

    # ======================================================
    # LANGKAH 2: PENGGAMBARAN (Rendering)
    # ======================================================
    
    current_x = START_X # Kursor X, akan bergeser ke kanan tiap kolom
    
    # Loop Kolom (Horizontal, i=0..n-1)
    for i in range(n):
        # Ambil lebar khusus untuk kolom ini
        this_col_width = col_widths[i]
        
        # Loop Baris/Tinggi (Vertikal, length=1..sisa)
        # Menggambar tumpukan kotak ke atas menyerupai tangga
        for length in range(1, n - i + 1):
            j = i + length - 1
            
            # Hitung Koordinat Kotak
            x1 = current_x
            x2 = current_x + this_col_width
            
            # Y dihitung dari bawah ke atas
            y2 = BASE_Y - ((length - 1) * BOX_HEIGHT) # Sisi bawah
            y1 = y2 - BOX_HEIGHT                      # Sisi atas
            
            # Siapkan teks isi sel
            if table[i][j]:
                isi_teks = ", ".join(sorted(list(table[i][j])))
            else:
                isi_teks = "-" # Tanda strip untuk sel kosong/invalid
            
            # Gambar Persegi Panjang (Kotak)
            canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_BOX, outline="black", width=1.5)
            
            # Logika Font Size: Kecilkan font jika teks terlalu panjang agar muat
            font_size = 9 if len(isi_teks) > 20 else 11
            
            # Tulis Teks di tengah kotak
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=isi_teks, fill=COLOR_TEXT, font=("Arial", font_size, "bold"))

        # --- GAMBAR KATA TOKEN DI BAGIAN BAWAH ---
        y_text = BASE_Y + 25 # Sedikit di bawah kotak terbawah
        x_center = current_x + (this_col_width / 2) # Tengah kolom
        canvas.create_text(x_center, y_text, text=tokens[i], fill="black", font=("Arial", 12, "italic"))
        
        # Geser kursor X untuk menggambar kolom berikutnya
        current_x += this_col_width

def reset_gui():
    """Mengembalikan GUI ke kondisi awal (bersih)."""
    entry_kalimat.delete(0, tk.END) # Hapus input
    canvas_output.delete("all")     # Hapus gambar
    lbl_status.config(text="STATUS: MENUNGGU INPUT", fg="black") # Reset label

# ==========================================
# KONFIGURASI JENDELA UTAMA (MAIN WINDOW)
# ==========================================
root = tk.Tk() # Membuat instance window utama
root.title("Aplikasi Parsing Kalimat Bahasa Bali Berpredikat Frasa Adjektiva (Algoritma CYK)")
root.geometry("900x700") # Ukuran awal jendela

# Inisialisasi Grammar satu kali saat aplikasi mulai
my_grammar = get_bali_grammar() 

# --- ELEMEN UI: JUDUL ---
lbl_judul = tk.Label(root, text="PARSER KALIMAT BAHASA BALI\nBERPREDIKAT FRASA ADJEKTIVA", font=("Helvetica", 16, "bold"))
lbl_judul.pack(pady=10)

# --- ELEMEN UI: INPUT AREA ---
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

lbl_instruksi = tk.Label(frame_input, text="Masukkan Kalimat:")
lbl_instruksi.pack(side=tk.LEFT, padx=5)

entry_kalimat = tk.Entry(frame_input, width=50, font=("Arial", 12))
entry_kalimat.pack(side=tk.LEFT, padx=5)
# Binding tombol Enter keyboard untuk memicu proses
entry_kalimat.bind('<Return>', lambda event: proses_gui()) 

# --- ELEMEN UI: TOMBOL AKSI ---
frame_tombol = tk.Frame(root)
frame_tombol.pack(pady=10)

# Tombol Cek (Hijau)
btn_proses = tk.Button(frame_tombol, text="CEK KALIMAT", command=proses_gui, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_proses.pack(side=tk.LEFT, padx=10)

# Tombol Reset (Merah)
btn_reset = tk.Button(frame_tombol, text="RESET", command=reset_gui, bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_reset.pack(side=tk.LEFT, padx=10)

# --- ELEMEN UI: LABEL STATUS ---
lbl_status = tk.Label(root, text="STATUS: MENUNGGU INPUT", font=("Arial", 12, "bold"), fg="black")
lbl_status.pack(pady=5)

# --- ELEMEN UI: AREA GAMBAR (CANVAS) ---
# Menggunakan Frame dengan Scrollbar agar piramida besar bisa dilihat
frame_canvas = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Scrollbar Vertikal & Horizontal
v_scroll = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL)
h_scroll = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)

# Canvas Widget (Tempat menggambar)
canvas_output = tk.Canvas(frame_canvas, bg="white", xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

# Hubungkan Scrollbar dengan Canvas
v_scroll.config(command=canvas_output.yview)
h_scroll.config(command=canvas_output.xview)

# Penempatan (Packing) elemen Canvas dan Scrollbar
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
canvas_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Mulai Loop Utama GUI
root.mainloop()