# ==============================================================================
# Deskripsi: Antarmuka Grafis (GUI) untuk aplikasi Parser Bahasa Bali.
#            Menggunakan Tkinter untuk input pengguna dan visualisasi tabel.
# ==============================================================================

import tkinter as tk
from tkinter import scrolledtext, messagebox
# Mengimpor fungsi logika dari file Program_CYK_Table.py
from Program_CYK_Table import get_bali_grammar, cyk_parse, get_cyk_table_string


# =========================================================================
#  MODUL PARSE TREE (POHON PENURUNAN)
# =========================================================================

def get_parse_tree_structure(grammar, table, tokens):
    """
    Mengubah Tabel CYK menjadi struktur data Pohon (Nested Tuple) secara rekursif.
    Output: ('K', ('P', '...'), ('S', '...'))
    """
    n = len(tokens)
    
    def backtrack(simbol, i, j):
        # 1. BASIS: Jika Daun (Kata Asli)
        if i == j:
            # Kembalikan tuple (Simbol, Kata_Asli)
            return (simbol, tokens[i])

        # 2. REKURSI: Cari pembentuk (Anak)
        if simbol in grammar:
            for rhs in grammar[simbol]:
                if len(rhs) == 2: # Hanya aturan biner A -> B C
                    B, C = rhs[0], rhs[1]
                    # Cari titik potong k
                    for k in range(i, j):
                        if B in table[i][k] and C in table[k+1][j]:
                            # REKURSI KE ANAK
                            left_node = backtrack(B, i, k)
                            right_node = backtrack(C, k+1, j)
                            
                            # Jika jalur ini valid (tidak buntu)
                            if left_node and right_node:
                                return (simbol, left_node, right_node)
        return None

    # Mulai dari simbol Start 'K' di puncak tabel
    if 'K' in table[0][n-1]:
        return backtrack('K', 0, n-1)
    return None

def open_parse_tree_window(root_window, tree_structure, tokens):
    """
    Membuka jendela popup Parse Tree dengan algoritma tata letak 'Bottom-Up'.
    Posisi X node dihitung berdasarkan posisi kata, mencegah tumpang tindih.
    """
    if not tree_structure:
        messagebox.showerror("Error", "Gagal membentuk struktur pohon!")
        return

    tree_win = tk.Toplevel(root_window)
    tree_win.title("Parse Tree & Pola Kalimat")
    
    # KONFIGURASI JARAK
    X_SPACING = 140       # Jarak horizontal antar kata (diperlebar agar aman)
    Y_SPACING = 100       # Jarak vertikal antar level
    START_Y = 60          # Margin atas
    
    # Hitung lebar total canvas berdasarkan jumlah kata
    # Minimal 800px biar tidak kekecilan
    total_width = max(800, len(tokens) * X_SPACING + 100)
    total_height = max(600, (len(tokens) * 50) + 200) # Estimasi tinggi
    
    # Setup Window & Canvas
    window_width = min(1300, total_width + 50)
    tree_win.geometry(f"{window_width}x650")
    
    c = tk.Canvas(tree_win, bg="white", scrollregion=(0, 0, total_width, total_height))
    
    hbar = tk.Scrollbar(tree_win, orient=tk.HORIZONTAL, command=c.xview)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    vbar = tk.Scrollbar(tree_win, orient=tk.VERTICAL, command=c.yview)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    c.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    c.pack(fill=tk.BOTH, expand=True)

    # --- VARIABEL PELACAK POSISI ---
    # Kita gunakan list mutable agar bisa diubah di dalam fungsi rekursif
    # leaf_tracker[0] akan menyimpan indeks kata ke-berapa yang sedang diproses
    leaf_tracker = [0] 

    def recursive_draw(node, current_y):
        """
        Fungsi Rekursif Pintar:
        1. Turun ke bawah dulu sampai ketemu kata (Daun).
        2. Tentukan posisi X kata berdasarkan urutan.
        3. Posisi Parent adalah rata-rata dari posisi Children.
        4. Return posisi X node ini ke pemanggilnya.
        """
        label = node[0]
        my_x = 0
        
        # --- KASUS 1: NODE CABANG BINER (Punya Kiri & Kanan) ---
        if len(node) == 3:
            left_child = node[1]
            right_child = node[2]
            
            # Rekursi ke anak kiri & kanan untuk dapatkan posisi X mereka
            x_left = recursive_draw(left_child, current_y + Y_SPACING)
            x_right = recursive_draw(right_child, current_y + Y_SPACING)
            
            # Posisi saya ada di tengah-tengah anak
            my_x = (x_left + x_right) / 2
            
            # Gambar Garis ke Anak
            # Garis digambar DULUAN supaya tertimpa oleh oval (jadi rapi)
            c.create_line(my_x, current_y + 20, x_left, current_y + Y_SPACING - 20, fill="gray", width=2)
            c.create_line(my_x, current_y + 20, x_right, current_y + Y_SPACING - 20, fill="gray", width=2)

        # --- KASUS 2: NODE DAUN (Label -> Kata) ---
        # Bisa format ('NP', 'buku') atau ('NP', ('Noun', 'buku')) -> Unary
        # Kita cek apakah elemen kedua adalah String (Kata)
        elif len(node) == 2 and isinstance(node[1], str):
            kata = node[1]
            
            # Hitung X berdasarkan urutan kata (Leaf Index)
            # Rumus: Margin Kiri + (Urutan * Jarak)
            my_x = 80 + (leaf_tracker[0] * X_SPACING)
            
            # Naikkan counter untuk kata berikutnya
            leaf_tracker[0] += 1
            
            # Gambar Garis Putus-putus ke Kata
            y_kata = current_y + 60
            c.create_line(my_x, current_y + 20, my_x, y_kata - 10, fill="black", dash=(2, 2))
            
            # Teks Kata Asli (Biru Miring)
            c.create_text(my_x, y_kata, text=kata, font=("Arial", 11, "italic", "bold"), fill="blue")

        # --- KASUS 3: NODE UNARY (Label -> Node Lain) ---
        # Contoh: NP -> Pronoun (tanpa cabang lain)
        elif len(node) == 2 and isinstance(node[1], tuple):
            child_node = node[1]
            
            # Rekursi lurus ke bawah
            x_child = recursive_draw(child_node, current_y + Y_SPACING)
            
            # Posisi X saya sama dengan anak (lurus vertikal)
            my_x = x_child
            
            # Gambar Garis Lurus
            c.create_line(my_x, current_y + 20, x_child, current_y + Y_SPACING - 20, fill="gray", width=2)

        # --- MENGGAMBAR OVAL (NODE) ---
        # Ukuran Oval Dinamis mengikuti panjang teks
        text_len = len(label)
        radius_x = max(24, (text_len * 6) + 12) # Lebar menyesuaikan teks
        radius_y = 20
        
        c.create_oval(my_x - radius_x, current_y - radius_y, 
                      my_x + radius_x, current_y + radius_y, 
                      fill="#E0F7FA", outline="black", width=1.5)
        
        c.create_text(my_x, current_y, text=label, font=("Arial", 10, "bold"))
        
        # Kembalikan posisi X saya agar Parent di atas bisa menghitung tengahnya
        return my_x

    # MULAI PROSES GAMBAR DARI ROOT
    # Root ditaruh di START_Y, posisi X-nya akan otomatis dihitung oleh fungsi
    recursive_draw(tree_structure, START_Y)


hasil_tree_terakhir = None

def proses_gui():
    """
    Fungsi callback yang dipanggil saat tombol 'CEK KALIMAT' ditekan.
    Mengambil input, menjalankan parser, dan memperbarui GUI.
    """

    global hasil_tree_terakhir

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
        # Generate Struktur Tree & Aktifkan Tombol
        # Kita simpan datanya ke variabel global
        hasil_tree_terakhir = get_parse_tree_structure(my_grammar, table_hasil, tokens_baru)

        # Aktifkan tombol
        if 'btn_tree' in globals(): 
            btn_tree.config(state=tk.NORMAL, bg="#2196F3")

    else:
        lbl_status.config(text="STATUS: INVALID (DITOLAK)", fg="red")
        #Reset Tree & Matikan Tombol
        hasil_tree_terakhir = None

        # Matikan tombol karena kalimat salah
        if 'btn_tree' in globals():
            btn_tree.config(state=tk.DISABLED, bg="gray")

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

def aksi_lihat_tree():
    kalimat_input = entry_kalimat.get()
    tokens = kalimat_input.strip().lower().split()

    if hasil_tree_terakhir:
        open_parse_tree_window(root, hasil_tree_terakhir,tokens)
    else:
        messagebox.showinfo("Info", "Silakan proses kalimat valid terlebih dahulu.")

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

#Tombol lihat tree (Biru)
btn_tree = tk.Button(frame_tombol, text="LIHAT PARSE TREE", command=aksi_lihat_tree, 
                     bg="gray", fg="white", font=("Arial", 10, "bold"), padx=15, state=tk.DISABLED)
btn_tree.pack(side=tk.LEFT, padx=5)

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