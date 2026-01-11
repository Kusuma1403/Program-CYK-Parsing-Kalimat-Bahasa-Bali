import tkinter as tk
from tkinter import scrolledtext, messagebox
from Program_CYK_Table import get_bali_grammar, cyk_parse, get_cyk_table_string

# --- PASTIKAN FUNGSI LOGIKA CYK ANDA SUDAH ADA DI SINI ATAU DI-IMPORT ---
# from logika_cyk import cyk_parse, get_bali_grammar, get_cyk_table_string
# (Jika digabung dalam satu file, biarkan saja kode logika di atas)

def proses_gui():
    kalimat_input = entry_kalimat.get()
    
    if not kalimat_input.strip():
        messagebox.showwarning("Peringatan", "Mohon masukkan kalimat!")
        return

    kalimat_bersih = kalimat_input.strip().lower()
    tokens = kalimat_bersih.split()
    
    # Jalankan CYK
    is_valid, table_hasil = cyk_parse(kalimat_bersih, my_grammar)
    
    # Gambar hasilnya di Canvas
    gambar_piramida(canvas_output, table_hasil, tokens)
    
    # Update Status
    if is_valid:
        lbl_status.config(text="STATUS: VALID (DITERIMA)", fg="green")
    else:
        lbl_status.config(text="STATUS: INVALID (DITOLAK)", fg="red")

def gambar_piramida(canvas, table, tokens):
    """
    Fungsi menggambar tabel CYK Rata Kiri dengan LEBAR DINAMIS.
    Lebar kotak menyesuaikan panjang teks di dalamnya.
    """
    canvas.delete("all") 
    
    n = len(tokens)
    if n == 0: return

    # --- KONFIGURASI DASAR ---
    BOX_HEIGHT = 50       # Tinggi kotak tetap
    START_X = 50          # Margin kiri
    BASE_Y = 50 + (n * BOX_HEIGHT) 
    
    COLOR_BOX = "#FFE4C4" 
    COLOR_TEXT = "black"

    # ======================================================
    # LANGKAH 1: HITUNG LEBAR SETIAP KOLOM (PRE-CALCULATION)
    # ======================================================
    col_widths = [] # Menyimpan lebar untuk setiap kolom (0 sampai n-1)

    for i in range(n):
        # Cari teks terpanjang di kolom 'i' (termasuk kata inputnya)
        max_char_len = len(tokens[i]) 
        
        # Cek setiap kotak di atas kolom ini
        for length in range(1, n - i + 1):
            j = i + length - 1
            if table[i][j]:
                isi = ", ".join(sorted(list(table[i][j])))
                max_char_len = max(max_char_len, len(isi))
        
        # Rumus Lebar: (Jumlah Karakter * 9 pixel) + Padding 20px
        # Tapi minimal lebar 100px agar tidak terlalu gepeng untuk kata pendek
        calculated_width = max(100, (max_char_len * 9) + 20)
        col_widths.append(calculated_width)

    # Update scrollregion berdasarkan total lebar dinamis
    total_width = sum(col_widths) + 100
    total_height = (n * BOX_HEIGHT) + 150
    canvas.config(scrollregion=(0, 0, total_width, total_height))

    # ======================================================
    # LANGKAH 2: GAMBAR KOTAK MENGGUNAKAN LEBAR DINAMIS
    # ======================================================
    
    current_x = START_X # Pointer X yang akan bergerak ke kanan
    
    for i in range(n):
        # Ambil lebar khusus untuk kolom ini
        this_col_width = col_widths[i]
        
        # Loop ke atas (Tumpukan Tangga)
        for length in range(1, n - i + 1):
            j = i + length - 1
            
            # Koordinat X (Menggunakan current_x)
            x1 = current_x
            x2 = current_x + this_col_width
            
            # Koordinat Y (Tetap sama logikanya)
            y2 = BASE_Y - ((length - 1) * BOX_HEIGHT)
            y1 = y2 - BOX_HEIGHT
            
            # Isi Teks
            if table[i][j]:
                isi_teks = ", ".join(sorted(list(table[i][j])))
            else:
                isi_teks = "-"
            
            # Gambar Kotak
            canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_BOX, outline="black", width=1.5)
            
            # Gambar Teks (Ukuran font menyesuaikan sedikit)
            # Jika teks sangat panjang (>20 char), kecilkan font
            font_size = 9 if len(isi_teks) > 20 else 11
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=isi_teks, fill=COLOR_TEXT, font=("Arial", font_size, "bold"))

        # --- GAMBAR KATA DI BAWAH ---
        y_text = BASE_Y + 25
        x_center = current_x + (this_col_width / 2)
        canvas.create_text(x_center, y_text, text=tokens[i], fill="black", font=("Arial", 12, "italic"))
        
        # Geser pointer X untuk kolom berikutnya
        current_x += this_col_width

def reset_gui():
    entry_kalimat.delete(0, tk.END)
    canvas_output.delete("all")
    lbl_status.config(text="STATUS: MENUNGGU INPUT", fg="black")
# ==========================================
# KONFIGURASI JENDELA UTAMA (WINDOW)
# ==========================================
root = tk.Tk()
root.title("Aplikasi Parsing Bahasa Bali (Algoritma CYK)")
root.geometry("900x700") # Lebar x Tinggi

# Load Grammar (PENTING: Pastikan ini dipanggil sebelum GUI jalan)
# Ganti dengan pemanggilan fungsi grammar Anda yang sebenarnya
my_grammar = get_bali_grammar() 

# --- JUDUL ---
lbl_judul = tk.Label(root, text="PARSER KALIMAT BAHASA BALI", font=("Helvetica", 16, "bold"))
lbl_judul.pack(pady=10)

# --- FRAME INPUT ---
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

lbl_instruksi = tk.Label(frame_input, text="Masukkan Kalimat:")
lbl_instruksi.pack(side=tk.LEFT, padx=5)

entry_kalimat = tk.Entry(frame_input, width=50, font=("Arial", 12))
entry_kalimat.pack(side=tk.LEFT, padx=5)
entry_kalimat.bind('<Return>', lambda event: proses_gui()) # Tekan Enter untuk proses

# --- TOMBOL ---
frame_tombol = tk.Frame(root)
frame_tombol.pack(pady=10)

btn_proses = tk.Button(frame_tombol, text="CEK KALIMAT", command=proses_gui, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_proses.pack(side=tk.LEFT, padx=10)

btn_reset = tk.Button(frame_tombol, text="RESET", command=reset_gui, bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_reset.pack(side=tk.LEFT, padx=10)

# --- STATUS ---
lbl_status = tk.Label(root, text="STATUS: MENUNGGU INPUT", font=("Arial", 12, "bold"), fg="black")
lbl_status.pack(pady=5)

# --- AREA CANVAS DENGAN SCROLLBAR (PENTING UNTUK PIRAMIDA BESAR) ---
frame_canvas = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Scrollbar
v_scroll = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL)
h_scroll = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)

# Canvas Widget
canvas_output = tk.Canvas(frame_canvas, bg="white", xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

v_scroll.config(command=canvas_output.yview)
h_scroll.config(command=canvas_output.xview)

v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
canvas_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Jalankan
root.mainloop()