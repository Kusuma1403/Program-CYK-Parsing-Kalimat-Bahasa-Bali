def get_bali_grammar():
    """
    Mendefinisikan Grammar Bahasa Bali dalam bentuk CNF.
    Nama 'Dayu Gek' telah diganti menjadi 'Widya'.
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
    
    # Penggantian: 'Dayu Gek' -> 'widya'
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
    list_adj_time = ["cerik"] # Sesuai prompt
    list_num = ["sabilang"]

    # --- 2. LOGIKA FLATTENING (S, Pel, NP inherit terminal) ---
    # Sesuai instruksi: Kata di NP masuk ke terminal S dan Pel
    # Komponen NP biasanya: Noun, Pronoun, PropNoun, Part, Det
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
    tokens = sentence.lower().split()
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

def get_cyk_table_string(table, tokens):
    """
    Sama seperti print_cyk_boxed, tapi mengembalikan STRING (teks),
    bukan langsung print ke terminal.
    """
    import io
    output_buffer = io.StringIO() # Membuat penampung teks sementara
    
    n = len(tokens)
    
    # --- LOGIKA SAMA SEPERTI SEBELUMNYA ---
    display_grid = [['' for _ in range(n)] for _ in range(n)]
    max_len = 0
    for i in range(n):
        for j in range(n):
            if table[i][j]:
                content = ",".join(sorted(list(table[i][j])))
            else:
                content = ""
            display_grid[i][j] = content
            max_len = max(max_len, len(content))
    
    box_width = max(max_len, 4) + 2 

    # Tulis ke buffer, bukan print
    output_buffer.write("\nVISUALISASI TABEL CYK:\n")
    
    for length in range(n, 0, -1):
        row_top = []
        row_mid = []
        row_bot = []
        
        for i in range(n - length + 1):
            j = i + length - 1
            content = display_grid[i][j]
            row_top.append(f"┌{'─'*box_width}┐")
            row_mid.append(f"│{content:^{box_width}}│")
            row_bot.append(f"└{'─'*box_width}┘")
        
        separator = " "
        line_top = separator.join(row_top)
        line_mid = separator.join(row_mid)
        line_bot = separator.join(row_bot)
        
        total_width = n * (box_width + 4) # Estimasi lebar
        
        # Tulis ke buffer
        output_buffer.write(f"{line_top:^{total_width}}\n")
        output_buffer.write(f"{line_mid:^{total_width}}\n")
        output_buffer.write(f"{line_bot:^{total_width}}\n")

    # Bagian Kata Bawah
    output_buffer.write("-" * total_width + "\n")
    word_row = []
    for word in tokens:
        word_row.append(f"{word:^{box_width+2}}")
    output_buffer.write(f"{''.join(word_row):^{total_width}}\n")
    output_buffer.write("-" * total_width + "\n")
    
    # Ambil seluruh teks dari buffer
    result_text = output_buffer.getvalue()
    output_buffer.close()
    return result_text

# ==========================================
# CONTOH PENGGUNAAN
# ==========================================

if __name__ == "__main__":
    # 1. Load Grammar
    my_grammar = get_bali_grammar()
    
    # 2. Input Kalimat Uji Coba
    # Contoh kalimat: "Jegeg sajan widya punika"
    # P (AdjP Adv) + S (NP Det)
    
    kalimat_input = "demen tiang teken adi   "
    
    print(f"Memproses Kalimat: '{kalimat_input}'")
    
    # 3. Jalankan CYK
    diterima, tabel_hasil = cyk_parse(kalimat_input, my_grammar)
    
    # 4. Hasil
    get_cyk_table_string(tabel_hasil, kalimat_input.split())
    
    if diterima:
        print("\n[HASIL] Kalimat VALID (Diterima oleh Grammar)")
        print("Simbol 'K' ditemukan di puncak tabel.")
    else:
        print("\n[HASIL] Kalimat TIDAK VALID (Ditolak)")