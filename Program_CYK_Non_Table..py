def get_bali_grammar():
    """
    Mendefinisikan Grammar Bahasa Bali dalam bentuk CNF.
    Semua terminal dalam huruf kecil.
    """
    
    # --- 1. DAFTAR KATA (LEXICON) ---
    # Kita definisikan list kata dulu agar mudah dikelola dan digabung
    
    list_adj = [
        "jegeg", "lanying", "peteng", "dedet", "lantang", "tegeh", "cenik", 
        "kedas", "nyalang", "joh", "ening", "seger", "resik", "becik", "sungkan",
        "wicaksana", "putih", "tenang", "aget", "kasub", "gede", "demen", 
        "seleg", "melah", "pait", "gedeg", "tresna", "bhakti", "dueg", "sayang", 
        "jejeh", "kangen", "makesiab", "jemet", "penting", "seneng", "perlu", 
        "gelis", "satinut", "galak", "lek", "demit", "miik", "ngalub", "ririh", 
        "inguh", "rajin", "bengkung", "siteng", "nau", "wareg", "sebet", "cerik"
    ]
    
    list_adv = ["sajan", "pisan", "gati"]
    
    list_noun = [
        "cunguhipune", "kamar", "bokne", "punyane", "umah", "kacane", "yeh", 
        "tukade", "griya", "kaki", "prabu", "rabi", "panyingakan", "dadong", 
        "manah", "galah", "wastan", "umahne", "lawar", "basa", "inggris", 
        "bajune", "ubad", "adine", "timpalne", "putranipun", "guru", "panakne", 
        "meme", "buku", "cicing", "anak", "keluarga", "pan", "pikobet", 
        "pitulungan", "anake", "aturan", "desa", "sekolah", "tamiu", "cicingne", 
        "parumahan", "yoga", "natah", "bunga", "sandat", "jumah", "piutang", 
        "jumahne", "lontar", "karya", "idupne", "rerame", "kayu", "peken", 
        "kebaya", "pura", "nasi", "paon", "atine"
    ]
    
    list_prop_noun = [
        "widya", "putu", "made", "wayan", "nukarna", "bagya", "yogi", "kevin"
    ]
    
    list_pronoun = ["ida", "titiang", "dane", "ragane", "tiang", "ia", "raga"]
    list_det = ["punika", "puniki", "ento", "niki"]
    list_part = ["i", "sang"]
    list_prep = ["teken", "ring", "ajak", "uli", "di", "saking", "ka"]
    
    list_verb = [
        "polih", "ngajeng", "malajah", "memaca", "maan", "nepukin", "ngigel", 
        "musik", "karaosang", "ngasuh", "melaib", "manutur", "megending", 
        "mamaca", "ngidih", "tulung", "makidihan", "ngebekin", "magending", 
        "ngitungang", "nyurat", "ngamargiang", "negen", "nganggon", "nongos"
    ]
    
    list_noun_time = ["dibi", "ibi", "dugas", "sanja", "semeng", "jani", "tuni"]
    list_adj_time = ["cerik"]
    list_num = ["sabilang"]

    # --- 2. LOGIKA FLATTENING (S, Pel, NP inherit terminal) ---
    # Kata di NP masuk ke terminal S dan Pel
    # Komponen NP: Noun, Pronoun, PropNoun, Part, Det
    terminals_np = list_noun + list_prop_noun + list_pronoun + list_part + list_det
    
    # S dan Pel juga bisa punya terminal sendiri sesuai CFG awal, 
    # tapi kita gabungkan terminals_np ke dalamnya.
    terminals_s = terminals_np # S -> NP (Flattened)
    
    # Pel bisa berupa NP, tapi juga bisa Verb (Pel -> VP -> Verb)
    terminals_pel = terminals_np + list_verb + list_noun_time + list_prop_noun 

    # --- 3. STRUKTUR GRAMMAR (DICTIONARY) ---
    grammar = {
        # -- ATURAN UTAMA K (Variable Rules) --
        "K": [["P", "S"], ["X1", "S"], ["P", "X2"], ["X3", "Ket"], ["X4", "Ket"]],
        
        # -- VARIABEL BANTUAN --
        "X1": [["P", "Pel"]],
        "X2": [["S", "Pel"]],
        "X3": [["X1", "S"]],
        "X4": [["P", "X2"]],
        
        # -- PREDIKAT & FRASA ADJEKTIVA --
        "P": [["AdjP", "Adv"], ["AdjP", "Adj"]] + [[w] for w in list_adj], # P -> AdjP (Flattened to Adj)
        "AdjP": [["AdjP", "Adv"], ["AdjP", "Adj"]] + [[w] for w in list_adj],
        "Adv": [[w] for w in list_adv],
        "Adj": [[w] for w in list_adj],
        
        # -- SUBJEK (S) --
        "S": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
              ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"]] + [[w] for w in terminals_s],
              
        # -- PELENGKAP (Pel) --
        "Pel": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
                ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"], # NP rules
                ["VP", "NP"], ["VP", "Verb"], ["Prep", "NP"], 
                ["Prep", "Adj_time"], ["Prep", "NP_time"], ["PP", "PP"]] + [[w] for w in terminals_pel],
                
        # -- KETERANGAN (Ket) --
        "Ket": [["Prep", "NP"], ["Prep", "Adj_time"], ["Prep", "NP_time"], 
                ["PP", "PP"], ["NP_time", "Noun_time"], ["NP_time", "Det"], 
                ["NumP", "NP_time"], ["PP", "NP_time"]] + [[w] for w in list_noun_time],
        
        # -- FRASA NOMINA (NP) --
        "NP": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
               ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"]] + [[w] for w in terminals_np],
               
        # -- FRASA LAINNYA --
        "VP": [["VP", "NP"], ["VP", "Verb"]] + [[w] for w in list_verb],
        "PP": [["Prep", "NP"], ["Prep", "Adj_time"], ["Prep", "NP_time"], ["PP", "PP"]],
        "NumP": [["NumP", "NP_time"]] + [[w] for w in list_num],
        "NP_time": [["NP_time", "Noun_time"], ["NP_time", "Det"]] + [[w] for w in list_noun_time],
        
        # -- TERMINAL MURNI --
        "Noun": [[w] for w in list_noun],
        "Verb": [[w] for w in list_verb],
        "PropNoun": [[w] for w in list_prop_noun],
        "Pronoun": [[w] for w in list_pronoun],
        "Det": [[w] for w in list_det],
        "Part": [[w] for w in list_part],
        "Prep": [[w] for w in list_prep],
        "Num": [[w] for w in list_num],
        "Noun_time": [[w] for w in list_noun_time],
        "Adj_time": [[w] for w in list_adj_time]
    }
    
    return grammar

def cyk_parse(sentence, grammar):
    """
    Melakukan parsing kalimat menggunakan algoritma CYK.
    """
    # Tokenisasi (Split spasi & lowercase)
    tokens = sentence.lower().strip().split()
    n = len(tokens)
    
    if n == 0:
        return False, []

    # Inisialisasi Tabel Segitiga (n x n)
    table = [[set() for _ in range(n)] for _ in range(n)]
    
    # --- TAHAP 1: MENGISI TERMINAL (Baris Bawah) ---
    for i in range(n):
        word = tokens[i]
        found = False
        for lhs, rules in grammar.items():
            for rhs in rules:
                # Cek jika aturan adalah terminal (panjang 1) dan cocok dengan kata
                if len(rhs) == 1 and rhs[0] == word:
                    table[i][i].add(lhs)
                    found = True
        
        if not found:
            print(f"Peringatan: Kata '{word}' tidak ditemukan dalam Lexicon grammar.")

    # --- TAHAP 2: MENGISI KOMBINASI (Bottom-Up) ---
    for length in range(2, n + 1):  # Panjang substring 2 sampai n
        for i in range(n - length + 1):
            j = i + length - 1
            
            # Coba semua titik potong k
            for k in range(i, j):
                left_cell = table[i][k]
                right_cell = table[k + 1][j]
                
                # Cek aturan produksi A -> BC
                for lhs, rules in grammar.items():
                    for rhs in rules:
                        if len(rhs) == 2:
                            B, C = rhs[0], rhs[1]
                            if B in left_cell and C in right_cell:
                                table[i][j].add(lhs)

    # --- TAHAP 3: PENGECEKAN FINAL ---
    # Cek apakah simbol awal 'K' ada di sel puncak table[0][n-1]
    is_accepted = "K" in table[0][n-1]
    return is_accepted, table


def run_batch_test(sentences, grammar):
    import time
    print("\n" + "="*85)
    print(f"{'NO':<4} | {'KALIMAT INPUT':<50} | {'STATUS':<10} | {'WAKTU (s)':<10}")
    print("="*85)
    
    jumlah_valid = 0
    total_data = len(sentences)
    
    for i, kalimat in enumerate(sentences):
        kalimat_bersih = kalimat.strip().lower()
        
        start_time = time.time()
        
        # PANGGIL FUNGSI CYK ANDA DISINI
        # Asumsi fungsi utama Anda bernama cyk_parse
        is_valid, _ = cyk_parse(kalimat_bersih, grammar) 
        
        durasi = time.time() - start_time
        
        if is_valid:
            status = "VALID"
            jumlah_valid += 1
        else:
            status = "INVALID"
            
        # Cetak hasil per baris
        print(f"{i+1:<4} | {kalimat_bersih:<50} | {status:<10} | {durasi:.5f}")

    # REKAPITULASI
    print("="*85)
    print(f"TOTAL DATA PENGUJIAN : {total_data}")
    print(f"DITERIMA (VALID)     : {jumlah_valid}")
    print(f"DITOLAK (INVALID)    : {total_data - jumlah_valid}")
    
    if total_data > 0:
        akurasi = (jumlah_valid / total_data) * 100
    else:
        akurasi = 0
        
    print(f"TINGKAT AKURASI      : {akurasi:.2f}%")
    print("="*85)


# def print_cyk_boxed(table, tokens):
#     """
#     Menampilkan tabel CYK dalam bentuk piramida dengan garis kotak (Border).
#     Tanpa library tambahan.
#     """
#     n = len(tokens)
    
#     # 1. PRE-PROCESSING: Siapkan isi sel
#     display_grid = [['' for _ in range(n)] for _ in range(n)]
#     max_len = 0
    
#     for i in range(n):
#         for j in range(n):
#             if table[i][j]:
#                 content = ",".join(sorted(list(table[i][j])))
#             else:
#                 content = "" # Kosongkan jika tidak ada isi
#             display_grid[i][j] = content
#             max_len = max(max_len, len(content))
    
#     # Lebar kotak minimal (biar tidak terlalu gepeng untuk kata pendek)
#     # Tambahkan padding kiri kanan (misal +2 spasi)
#     box_width = max(max_len, 4) + 2 

#     print("\nVISUALISASI TABEL CYK (BOX MODEL):")
    
#     # 2. MENCETAK PIRAMIDA
#     # Loop dari tingkat teratas (panjang n) ke bawah (panjang 1)
#     for length in range(n, 0, -1):
        
#         # --- Baris Atas Kotak (Top Border) ---
#         # Contoh: ┌──────┐ ┌──────┐
#         top_line = ""
#         for i in range(n - length + 1):
#             # Membuat spasi untuk indentasi agar membentuk piramida
#             # Setiap tingkat indentasinya bertambah setengah dari lebar kotak
#             # Ini trik visual agar terlihat di tengah
#             top_line += " " * (box_width // 2) if i == 0 else " " * box_width 
#             # Maaf, logika indentasi manual agak rumit. 
#             # Kita pakai pendekatan "Centered String" per baris saja agar lebih rapi.
            
#         # KITA UBAH PENDEKATAN: 
#         # Buat satu baris penuh string, lalu di-center.
        
#         # Bagian Atas Box
#         row_top = []
#         # Bagian Tengah (Isi)
#         row_mid = []
#         # Bagian Bawah Box
#         row_bot = []
        
#         for i in range(n - length + 1):
#             j = i + length - 1
#             content = display_grid[i][j]
            
#             # Karakter Unicode untuk kotak: ┌ ─ ┐ │ └ ┘
#             # Format: ┌──────┐
#             row_top.append(f"┌{'─'*box_width}┐")
            
#             # Format: │  K   │
#             row_mid.append(f"│{content:^{box_width}}│")
            
#             # Format: └──────┘
#             row_bot.append(f"└{'─'*box_width}┘")
        
#         # Gabungkan kotak-kotak dalam satu baris dengan spasi tipis
#         separator = " "  # Jarak antar kotak horisontal
#         line_top = separator.join(row_top)
#         line_mid = separator.join(row_mid)
#         line_bot = separator.join(row_bot)
        
#         # Cetak dengan Rata Tengah (Center) menyesuaikan lebar layar total
#         # Estimasi lebar total tabel = n * (box_width + 1)
#         total_width = n * (box_width + 4)
        
#         print(f"{line_top:^{total_width}}")
#         print(f"{line_mid:^{total_width}}")
#         print(f"{line_bot:^{total_width}}")
        
#         # Tidak perlu baris baru kosong karena kotak sudah tinggi

#     # 3. MENCETAK KATA INPUT
#     print("-" * total_width)
#     word_row = []
#     for word in tokens:
#         # Format kata agar pas di tengah kotak imajiner
#         # Perlu penyesuaian sedikit agar lurus dengan piramida
#         word_row.append(f"{word:^{box_width+2}}") # +2 untuk kompensasi border
    
#     print(f"{''.join(word_row):^{total_width}}")
#     print("-" * total_width)

# ==========================================
# CONTOH PENGGUNAAN
# ==========================================

if __name__ == "__main__":
    # 1. Load Grammar
    my_grammar = get_bali_grammar()

    nama_file = 'dataset.txt'

    print(f"Sedang mencoba membuka file: {nama_file} ...")
    
    # 2. Input Kalimat Uji Coba
    # Contoh kalimat: "Jegeg sajan widya punika"
    # P (AdjP Adv) + S (NP Det)
    
    try:
        # Membuka file txt
        with open(nama_file, 'r') as f:
            # Membaca baris per baris & menghapus baris kosong
            # line.strip() berguna menghapus "Enter" (\n) di akhir kalimat
            kalimat_uji = [line.strip() for line in f if line.strip()]
        
        jumlah_data = len(kalimat_uji)
        print(f"Berhasil memuat {jumlah_data} kalimat. Memulai pengujian...\n")
        
        # 3. Jalankan Fungsi Batch Test
        # (Pastikan Anda sudah mencopy fungsi 'run_batch_test' yang saya berikan sebelumnya)
        run_batch_test(kalimat_uji, my_grammar)

    except FileNotFoundError:
        print("\n[ERROR] File tidak ditemukan!")
        print(f"Pastikan file '{nama_file}' ada di folder yang sama dengan script python ini.")
        print("Atau cek apakah penulisan nama filenya sudah benar (misal: dataset.txt).")


    
    # print(f"Memproses Kalimat: '{kalimat_input}'")
    
    # 3. Jalankan CYK
    # diterima, tabel_hasil = cyk_parse(kalimat_input, my_grammar)
    
    # 4. Hasil
    # print_cyk_boxed(tabel_hasil, kalimat_input.split())
    
    # if diterima:
    #     print("\n[HASIL] Kalimat VALID (Diterima oleh Grammar)")
    #     print("Simbol 'K' ditemukan di puncak tabel.")
    # else:
    #     print("\n[HASIL] Kalimat TIDAK VALID (Ditolak)")