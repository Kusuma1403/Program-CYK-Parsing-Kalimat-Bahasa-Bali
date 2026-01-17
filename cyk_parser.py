# =======================================================================================
# Deskripsi: Berisi logika inti untuk parsing kalimat bahasa Bali berpredikat
#            frasa adjektiva (AdjP) menggunakan Algoritma CYK (Cocke-Kasami-Younger)
# =======================================================================================

def get_bali_grammar():
    """
    Fungsi ini mengembalikan dictionary yang berisi aturan tata bahasa (grammar)
    Bahasa Bali dalam bentuk Chomsky Normal Form (CNF).
    
    Returns:
        grammar (dict): Dictionary dengan Key = Non-Terminal (LHS/Sisi Kiri Aturan)
                        dan Value = List of Lists (RHS/Sisi Kanan Aturan).
    """
    
    # --- 1. DAFTAR KATA (LEXICON) ---
    # Mendefinisikan list kata dasar berdasarkan kategori sintaksisnya.
    # Semua kata menggunakan huruf kecil untuk konsistensi pencocokan string.
    
    # Kata Sifat (Adjective)
    list_adj = [
        "jegeg", "lanying", "peteng", "dedet", "lantang", "tegeh", "cenik", 
        "kedas", "nyalang", "joh", "ening", "seger", "resik", "becik", "sungkan",
        "wicaksana", "putih", "tenang", "aget", "kasub", "gede", "demen", 
        "seleg", "melah", "pait", "gedeg", "tresna", "bakti", "dueg", "sayang", 
        "jejeh", "kangen", "makesiab", "jemet", "penting", "seneng", "perlu", 
        "gelis", "satinut", "galak", "lek", "demit", "miik", "ngalub", "ririh", 
        "inguh", "rajin", "bengkung", "siteng", "nau", "wareg", "sebet", "cerik", "mekelo", "sue"
    ]
    
    # Kata Keterangan (Adverb)
    list_adv = ["sajan", "pisan", "gati", "sesai"]
    
    # Kata Benda (Noun) - Termasuk benda konkret dan abstrak
    list_noun = [
        "cunguh", "kamar", "bok", "punyan", "umah", "kaca", "yeh", 
        "tukad", "griya", "kaki", "prabu", "rabi", "panyingakan", "dadong", 
        "manah", "galah", "wastan", "lawar", "basa", 
        "baju", "ubad", "adi", "timpal", "okan", "guru", "panak", 
        "meme", "buku", "cicing", "anak", "kulawarga", "pan", "pikobet",
        "pitulung", "awig-awig", "desa", "sekolah", "tamiu",
        "parumahan", "yoga", "natah", "bunga", "sandat", "jumah", "piutang", 
        "lontar", "karya", "idup", "rerama", "kayu", "peken", 
        "kebaya", "pura", "nasi", "paon", "ati", "petani", "buah", "stroberi", "tegal", "agung", 
        "dagang", "canang", "bapa", "tetamian", "keris", "kemimitan", "paica", 
        "due", "kampuh", "sutra", "puri", "tukang", "tenun", "kain", "endek", 
        "wantilan", "gangsa", "pragina", "kelas", "paplajahan", "seni", "uyah", 
        "sanggah", "tanding", "tulis", "jukung", "sisin", "pasih", "mobil", 
        "lapangan", "perbekel", "tiban", "umur", "ubuhan", "meong", "meter", 
        "tembok", "jam", "rapat", "ujian", "pemangku", "ukud"
    ]
    
    # Nama Diri (Proper Noun)
    list_prop_noun = [
        "widya", "putu", "made", "wayan", "nukarna", "bagya", "yogi", "kevin", "inggris",
        "desak", "gede", "kadek", "sanur"   
    ]
    
    # Kata Ganti (Pronoun) - Termasuk akhiran kepemilikan (-ne, -e, dll)
    list_pronoun = ["ida", "titiang", "dane", "ragane", "tiang", "ia", "raga", "ipune", "nyane", "ne", "e"]

    # Kata Penunjuk (Determiner)
    list_det = ["punika", "puniki", "ento", "niki"]

    # Partikel Nama (Title/Particle)
    list_part = ["i", "sang"]

    # Kata Depan (Preposition)
    list_prep = ["teken", "ring", "ajak", "uli", "di", "saking", "ka"]
    
    # Kata Kerja (Verb)
    list_verb = [
        "polih", "ngajeng", "malajah", "maan", "nepukin", "ngigel", 
        "musik", "karaosang", "ngempu", "malaib", "masatua", 
        "mamaca", "ngidih", "tulung", "makidihang", "ngebekin", "magending", 
        "ngitungang", "nyurat", "ngamargiang", "negen", "nganggon", "nongos", "ngalapang",
        "nyilihang", "ngai", "nyetir", "nyalon", "dadi"
    ]
    
    # Kata Benda Waktu (Temporal Noun)
    list_noun_time = ["dibi", "ibi", "dugas", "sanja", "semeng", "jani", "tuni", "mani", "tengai"]

    # Kata Sifat Waktu (Temporal Adjective)
    list_adj_time = ["cerik"] 

    # Kata Bilangan (Numeral)
    list_num = ["sabilang","molas", "dasa", "akilo", "telu", "limang", "telung", "dua", "duang"]

    # --- 2. LOGIKA FLATTENING (Penyederhanaan Aturan Terminal) ---
    # CYK mengharuskan aturan dalam bentuk A -> a (Non-Terminal -> Terminal).
    # Agar aturan produksi lebih ringkas, kita gabungkan beberapa kategori kata
    # ke dalam variabel terminal gabungan.

    # Terminal untuk Frasa Nomina (NP): Gabungan Noun, PropNoun, Pronoun
    terminals_np = list_noun + list_prop_noun + list_pronoun
    
    # Terminal untuk Subjek (S): Subjek umumnya diisi oleh NP
    terminals_s = terminals_np # S -> NP (Flattened)
    
    # Terminal untuk Pelengkap (Pel): Pelengkap bisa berupa NP atau Verb
    terminals_pel = terminals_np + list_verb

    # --- 3. STRUKTUR GRAMMAR (DICTIONARY) ---
    # Mendefinisikan aturan produksi utama.
    # Format Key: "Non-Terminal"
    # Format Value: List of Lists, contoh: [["P", "S"], ["kata"]]

    grammar = {
        # -- ATURAN UTAMA KALIMAT (K) --
        # K -> P S           (Predikat Subjek)
        # K -> X1 S          (Pola P Pel S)
        # K -> P X2          (Pola P S Pel)
        # K -> X3 Ket        (Pola P Pel S Ket)
        # K -> X4 Ket        (Pola P S Pel Ket)
        "K": [["P", "S"], ["X1", "S"], ["P", "X2"], ["X3", "Ket"], ["X4", "Ket"]],
        
        # -- VARIABEL BANTUAN (Intermediary Variables) --
        # Diperlukan untuk memecah aturan panjang menjadi biner (max 2 non-terminals)
        "X1": [["P", "Pel"]],
        "X2": [["S", "Pel"]],
        "X3": [["X1", "S"]],
        "X4": [["P", "X2"]],
        
        # -- PREDIKAT (P) & FRASA ADJEKTIVA (AdjP) --
        # P -> AdjP Adv | AdjP Adj | Terminal (list_adj)
        # Kita gunakan list comprehension [[w] for w in ...] untuk membuat aturan terminal A -> a
        "P": [["AdjP", "Adv"], ["AdjP", "Adj"]] + [[w] for w in list_adj], # P -> AdjP (Flattened to Adj)
        "AdjP": [["AdjP", "Adv"], ["AdjP", "Adj"]] + [[w] for w in list_adj],
        "Adv": [[w] for w in list_adv],
        "Adj": [[w] for w in list_adj],
        
        # -- SUBJEK (S) --
        # Aturan S -> Struktur NP | Terminal (terminals_s)
        "S": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
              ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"]] + [[w] for w in terminals_s],
              
        # -- PELENGKAP (Pel) --
        # Pelengkap sangat fleksibel: bisa NP, VP, atau PP
        "Pel": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
                ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"], # NP rules
                ["VP", "NP"], ["VP", "Verb"], ["Prep", "NP"], 
                ["Prep", "Adj_time"], ["Prep", "NP_time"], ["PP", "PP"]] + [[w] for w in terminals_pel],
                
        # -- KETERANGAN (Ket) --
        # Keterangan waktu, tempat, cara
        "Ket": [["Prep", "NP"], ["Prep", "Adj_time"], ["Prep", "NP_time"], 
                ["PP", "PP"], ["NP_time", "Noun_time"], ["NP_time", "Det"], 
                ["NumP", "NP_time"], ["PP", "NP_time"]] + [[w] for w in list_noun_time] + [[w] for w in list_num],
        
        # -- FRASA NOMINA (NP) --
        "NP": [["NP", "Noun"], ["Part", "NP"], ["NP", "Det"], ["NP", "Pronoun"], 
               ["NP", "PropNoun"], ["NP", "Part"], ["NP", "AdjP"]] + [[w] for w in terminals_np],
               
       # -- FRASA VERBA (VP), PREPOSISI (PP), & LAINNYA --
        "VP": [["VP", "NP"], ["VP", "Verb"]] + [[w] for w in list_verb],
        "PP": [["Prep", "NP"], ["Prep", "Adj_time"], ["Prep", "NP_time"], ["PP", "PP"]],
        "NumP": [["NumP", "NP_time"]] + [[w] for w in list_num],
        "NP_time": [["NP_time", "Noun_time"], ["NP_time", "Det"]] + [[w] for w in list_noun_time],
        
        # -- TERMINAL MURNI (Dasar Leksikon) --
        # Aturan untuk menurunkan kategori leksikal langsung ke kata (misal: Noun -> 'buku')
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
    Implementasi algoritma CYK:
    1. Preprocessing: Memecah kalimat menjadi token/kata.
    2. Filling Diagonal: Mengisi baris pertama tabel dengan kategori kata tersebut.
    3. Filling Tables: Menggabungkan kategori-kategori secara bottom-up.

    Args:
        sentence (str): Kalimat input (misal: "Jegeg sajan Putu").
        grammar (dict): Aturan tata bahasa dari get_bali_grammar().

    Returns:
        is_accepted (bool): True jika kalimat valid, False jika tidak.
        table (list): Tabel segitiga (piramida) hasil parsing.
        tokens (list): Daftar token setelah preprocessing.
    """

    # 1. Preprocessing Input
    # Mengubah ke huruf kecil dan memisahkan kata berdasarkan spasi (tokenisasi)
    raw_words = sentence.lower().split()

    # Daftar akhiran yang dianggap sebagai Pronoun
    pronoun_suffixes = [x[0] for x in grammar.get("Pronoun", [])]
    tokens = []

    # --- Preprocessing: Penanganan Akhiran (Suffix) ---
    # Contoh: "cunguhne" -> "cunguh" + "ne"
    for word in raw_words:
        # --- LOGIKA 1: Cek apakah kata sudah ada di Grammar? ---
        word_is_known = False
        for lhs, rules in grammar.items():
            for rhs in rules:
                # Cek jika rule berbentuk terminal (panjang 1) dan katanya cocok
                if len(rhs) == 1 and rhs[0] == word:
                    word_is_known = True
                    break
            if word_is_known:
                break

        # Jika kata sudah dikenali (misal: "ipune" ada di lexicon), JANGAN dipisah.
        if word_is_known:
            tokens.append(word)
            continue # Lanjut ke kata berikutnya

        # --- LOGIKA 2: Jika tidak dikenal, Coba Pisahkan Akhiran ---
        split_found = False
        for s in pronoun_suffixes:
            # Cek apakah kata diakhiri suffix DAN kata tersebut bukan suffix itu sendiri
            if word.endswith(s) and word != s:
                stem = word[:-len(s)] # Ambil kata dasar (misal: cunguh)

                # Masukkan kata dasar dan akhiran sebagai token terpisah
                tokens.append(stem)
                tokens.append(s)
                split_found = True
                break # Stop jika sudah ketemu akhiran terpanjang

        # Jika tidak ada akhiran yang cocok, masukkan kata aslinya (meski tidak dikenal)
        if not split_found:
            tokens.append(word)

    n = len(tokens)

    # Jika input kosong, langsung return False
    if n == 0:
        return False, [], []

    # 2. Inisialisasi Tabel CYK
    # Membuat matriks n x n berisi himpunan kosong (set) di setiap selnya.
    # Sel table[i][j] akan menyimpan variabel non-terminal yang bisa menurunkan
    # substring dari indeks i sampai j.
    table = [[set() for _ in range(n)] for _ in range(n)]

    # --- TAHAP 1: MENGISI TERMINAL (DIAGONAL UTAMA) ---
    # Mengisi sel table[i][i] (panjang substring = 1).
    # Mencari aturan A -> 'kata' yang cocok dengan token di posisi i.
    for i in range(n):
        word = tokens[i]
        found = False
        for lhs, rules in grammar.items():
            for rhs in rules:
                # Cek jika aturan sisi kanan hanya berisi 1 elemen (terminal)
                # dan elemen tersebut sama dengan kata token.
                if len(rhs) == 1 and rhs[0] == word:
                    table[i][i].add(lhs)
                    found = True
        # Peringatan jika kata tidak dikenal (tidak ada di lexicon)
        if not found:
            print(f"Peringatan: Kata '{word}' tidak ditemukan dalam Lexicon grammar.")

    # --- TAHAP 2: MENGISI KOMBINASI (BOTTOM-UP) ---
    # Mengisi tabel untuk panjang substring mulai dari 2 sampai n.
    for length in range(2, n + 1):
        # Iterasi posisi awal substring (i)
        for i in range(n - length + 1):
            # Menentukan posisi akhir substring (j)
            j = i + length - 1

            # Iterasi titik potong (k) antara i dan j.
            # Substring akan dipecah menjadi dua bagian: [i...k] dan [k+1...j]
            for k in range(i, j):
                # Ambil himpunan variabel dari sel kiri (B) dan sel kanan (C)
                left_cell = table[i][k]         # Variabel untuk bagian pertama
                right_cell = table[k + 1][j]    # Variabel untuk bagian kedua

                # Cek setiap aturan produksi A -> BC di grammar
                for lhs, rules in grammar.items():
                    for rhs in rules:
                        # Pastikan aturan memiliki 2 non-terminal di sisi kanan
                        if len(rhs) == 2:
                            B, C = rhs[0], rhs[1]
                            # Jika B ada di sel kiri DAN C ada di sel kanan,
                            # maka A (lhs) bisa ditambahkan ke sel gabungan saat ini.
                            if B in left_cell and C in right_cell:
                                table[i][j].add(lhs)

    # --- TAHAP 3: PENGECEKAN FINAL ---
    # Kalimat valid jika simbol awal 'K' (Kalimat) ada di sel puncak table[0][n-1]
    is_accepted = "K" in table[0][n-1]

    return is_accepted, table, tokens

def get_parse_tree_structure(grammar, table, tokens):
    """
    Mengubah Tabel CYK menjadi struktur data Pohon (Nested Tuple) secara rekursif.
    Output contoh: ('K', ('P', 'jegeg'), ('S', 'tiang'))
    """
    n = len(tokens)

    # Fungsi pembantu rekursif di dalam (nested function)
    def backtrack(simbol, i, j):
        # 1. BASIS (Kondisi Berhenti): Jika i == j, berarti kita ada di level kata (Daun)
        #    Ini terjadi ketika panjang substring adalah 1.
        if i == j:
            # Kembalikan tuple (Simbol, Kata_Asli)
            # Contoh: ('Noun', 'buku')
            return (simbol, tokens[i])

        # 2. REKURSI: Cari aturan mana yang membentuk simbol ini
        if simbol in grammar:
            # Cek semua aturan produksi untuk simbol ini (misal K -> P S)
            for rhs in grammar[simbol]:

                # Kita hanya perhatikan aturan biner A -> B C (2 non-terminal di RHS) karena ini CNF
                if len(rhs) == 2:
                    B, C = rhs[0], rhs[1]

                    # Kita harus mencari titik potong 'k' yang valid.
                    # Loop dari KANAN ke KIRI (range mundur).
                    # Ini memprioritaskan "Anak Kiri Besar" (Greedy Left).
                    # Dengan loop mundur, kita cek k di posisi paling kanan dulu.
                    for k in range(j - 1, i - 1, -1):
                        if B in table[i][k] and C in table[k+1][j]:

                            # Jika ya, berarti kita menemukan jalurnya!
                            # Lakukan rekursi ke anak kiri (B) dan anak kanan (C)
                            left_node = backtrack(B, i, k)
                            right_node = backtrack(C, k+1, j)

                            # Jika kedua anak berhasil mengembalikan node (tidak None)
                            if left_node and right_node:
                                # Kembalikan struktur pohon: (Induk, AnakKiri, AnakKanan)
                                return (simbol, left_node, right_node)
        return None # Jika tidak ada jalur yang valid

    # Mulai proses dari simbol awal 'K' (Kalimat) yang ada di puncak tabel (0, n-1)
    if 'K' in table[0][n-1]:
        return backtrack('K', 0, n-1)

    return None # Jika simbol K tidak ada di puncak, berarti kalimat tidak valid

def get_cyk_table_string(table, tokens):
    """
    Fungsi utilitas untuk menghasilkan representasi STRING dari tabel CYK
    dalam format tabel ASCII yang rapi. Berguna untuk debugging atau output konsol.
    """
    import io
    output_buffer = io.StringIO() # Buffer string sementara

    n = len(tokens)

    # Membuat grid teks untuk setiap sel tabel
    display_grid = [['' for _ in range(n)] for _ in range(n)]
    max_len = 0
    for i in range(n):
        for j in range(n):
            if table[i][j]:
                # Gabungkan variabel dalam sel dengan koma, urutkan agar rapi
                content = ",".join(sorted(list(table[i][j])))
            else:
                content = ""
            display_grid[i][j] = content
            # Cari teks terpanjang untuk menentukan lebar kolom tabel
            max_len = max(max_len, len(content))

    # Set lebar kotak (minimal 4 karakter + padding)
    box_width = max(max_len, 4) + 2

    # Tulis ke buffer, bukan print
    output_buffer.write("\nVISUALISASI TABEL CYK:\n")

    # Loop mencetak baris dari puncak piramida (length=n) ke bawah (length=1)
    for length in range(n, 0, -1):
        row_top = [] # Garis atas kotak
        row_mid = [] # Isi teks kotak
        row_bot = [] # Garis bawah kotak

        for i in range(n - length + 1):
            j = i + length - 1
            content = display_grid[i][j]
            # Membuat kotak dengan karakter ASCII
            row_top.append(f"┌{'─'*box_width}┐")
            row_mid.append(f"│{content:^{box_width}}│") # Teks rata tengah
            row_bot.append(f"└{'─'*box_width}┘")

        # Gabungkan potongan kotak dalam satu baris
        separator = " "
        line_top = separator.join(row_top)
        line_mid = separator.join(row_mid)
        line_bot = separator.join(row_bot)

        # Hitung total lebar untuk perataan tengah (centering)
        total_width = n * (box_width + 4) # Estimasi lebar

        # Tulis ke buffer
        output_buffer.write(f"{line_top:^{total_width}}\n")
        output_buffer.write(f"{line_mid:^{total_width}}\n")
        output_buffer.write(f"{line_bot:^{total_width}}\n")

    # Mencetak kata-kata token di bagian paling bawah
    output_buffer.write("-" * total_width + "\n")
    word_row = []
    for word in tokens:
        word_row.append(f"{word:^{box_width+2}}")
    output_buffer.write(f"{''.join(word_row):^{total_width}}\n")
    output_buffer.write("-" * total_width + "\n")

    # Kembalikan string lengkap
    result_text = output_buffer.getvalue()
    output_buffer.close()
    return result_text

# ==========================================
# BLOK UTAMA (MAIN) UNTUK PENGUJIAN LANGSUNG
# ==========================================
if __name__ == "__main__":
    # 1. Memuat Grammar
    my_grammar = get_bali_grammar()

    # 2. Input Pengguna
    kalimat_input = input("Inputkan kalimat bahasa Bali: ").strip()
    print(f"Memproses Kalimat: '{kalimat_input}'")

    # 3. Eksekusi CYK
    # Perhatikan: sekarang menerima 3 return values
    diterima, tabel_hasil, tokens_baru = cyk_parse(kalimat_input, my_grammar)

    print(f"Token setelah preprocessing: {tokens_baru}")

    # 4. Tampilkan Visualisasi Teks (Gunakan tokens_baru)
    print(get_cyk_table_string(tabel_hasil, tokens_baru))

    # 5. Tampilkan Hasil Akhir
    if diterima:
        print("\n[HASIL] Kalimat VALID (Diterima oleh Grammar)")
        print("Simbol 'K' ditemukan di puncak tabel.")
    else:
        print("\n[HASIL] Kalimat TIDAK VALID (Ditolak)")