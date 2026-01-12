import customtkinter as ctk
import tkinter as tk
from cyk_parser import get_bali_grammar, cyk_parse, get_parse_tree_structure

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- THEME COLOR DEFINITIONS ---
THEME_COLORS = {
    "Dark": {
        "canvas_bg": "#2B2B2B",
        "box_fill": "#3A3A3A",
        "box_outline": "#555555",
        "text": "#E0E0E0",
        "token": "#2CC985",
        "k_text": "#FFD700",
        "k_fill": "#444444",
        "line": "#777777",
        "dash_line": "#555555",
        "node_fill": "#444444",
        "node_outline": "#2CC985",
        "node_text": "white",
        "empty_text": "#777777"
    },
    "Light": {
        "canvas_bg": "#F5F5F5",
        "box_fill": "#FFE4C4", # Bisque
        "box_outline": "#AAAAAA",
        "text": "black",
        "token": "#27AE60", # Darker green for contrast
        "k_text": "#D35400", # Burnt Orange for emphasis
        "k_fill": "#FFE4C4", # Same as box fill
        "line": "gray",
        "dash_line": "black",
        "node_fill": "#E0F7FA",
        "node_outline": "black",
        "node_text": "black",
        "empty_text": "#AAAAAA"
    }
}

class BaliParserApp(ctk.CTk):
    """
    Kelas utama GUI.
    Mewarisi CTk (CustomTkinter Window).
    """
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Parser Kalimat Bahasa Bali Berpredikat Frasa Adjektiva (Algoritma CYK)")
        self.geometry("1100x800")
        self.minsize(800, 600)

        # Initialize grammar
        self.grammar = get_bali_grammar()
        self.last_tree_structure = None
        self.last_table = None
        self.last_tokens = None
        self.current_theme_mode = "Dark" # Default

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Tabview expands

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1) # Spacer column

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="Parser Kalimat Bahasa Bali Berpredikat Frasa Adjektiva",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Theme Switcher
        self.switch_theme = ctk.CTkSwitch(
            self.header_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="Dark",
            offvalue="Light"
        )
        self.switch_theme.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        self.switch_theme.select() # Set switch to ON (Dark) initially

        # --- INPUT SECTION ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry_sentence = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Masukkan kalimat bahasa Bali (contoh: 'Cenik sajan umah punika')",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_sentence.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_sentence.bind('<Return>', lambda event: self.start_parsing())

        self.btn_parse = ctk.CTkButton(
            self.input_frame,
            text="Cek Kalimat",
            command=self.start_parsing,
            fg_color="#00a63e", # Green accent
            hover_color="#008236",
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_parse.grid(row=0, column=1, padx=5)

        self.btn_reset = ctk.CTkButton(
            self.input_frame,
            text="Reset",
            command=self.reset_app,
            fg_color="#e7000b", # Red accent
            hover_color="#c10007",
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_reset.grid(row=0, column=2, padx=5)

        # Status Label
        self.lbl_status = ctk.CTkLabel(
            self.input_frame,
            text="Menunggu input kalimat...",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.lbl_status.grid(row=1, column=0, columnspan=3, pady=(5, 0), sticky="w")

        # --- TABS ---
        self.tabview = ctk.CTkTabview(self, width=1000, height=600)
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.tabview._segmented_button.configure(
            height=45,  # tinggi tombol tab
            font=ctk.CTkFont(size=14, weight="bold")
        )

        self.tab_table = self.tabview.add("Triangular Table")
        self.tab_tree = self.tabview.add("Parse Tree")

        # Configure Tab 1: CYK Table (Canvas)
        self.tab_table.grid_columnconfigure(0, weight=1)
        self.tab_table.grid_rowconfigure(0, weight=1)

        # Standard Tkinter Canvas for complex drawing inside CustomTkinter Frame
        self.canvas_table = tk.Canvas(self.tab_table, bg=THEME_COLORS["Dark"]["canvas_bg"], highlightthickness=0)
        self.canvas_table.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for Table
        self.scroll_y_table = ctk.CTkScrollbar(self.tab_table, orientation="vertical", command=self.canvas_table.yview)
        self.scroll_y_table.grid(row=0, column=1, sticky="ns")
        self.scroll_x_table = ctk.CTkScrollbar(self.tab_table, orientation="horizontal", command=self.canvas_table.xview)
        self.scroll_x_table.grid(row=1, column=0, sticky="ew")
        self.canvas_table.configure(yscrollcommand=self.scroll_y_table.set, xscrollcommand=self.scroll_x_table.set)

        # Configure Tab 2: Parse Tree (Canvas)
        self.tab_tree.grid_columnconfigure(0, weight=1)
        self.tab_tree.grid_rowconfigure(0, weight=1)

        self.canvas_tree = tk.Canvas(self.tab_tree, bg=THEME_COLORS["Dark"]["canvas_bg"], highlightthickness=0)
        self.canvas_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for Tree
        self.scroll_y_tree = ctk.CTkScrollbar(self.tab_tree, orientation="vertical", command=self.canvas_tree.yview)
        self.scroll_y_tree.grid(row=0, column=1, sticky="ns")
        self.scroll_x_tree = ctk.CTkScrollbar(self.tab_tree, orientation="horizontal", command=self.canvas_tree.xview)
        self.scroll_x_tree.grid(row=1, column=0, sticky="ew")
        self.canvas_tree.configure(yscrollcommand=self.scroll_y_tree.set, xscrollcommand=self.scroll_x_tree.set)

    def toggle_theme(self):
        new_mode = self.switch_theme.get() # "Dark" or "Light"
        self.current_theme_mode = new_mode

        # 1. Update CustomTkinter appearance
        ctk.set_appearance_mode(new_mode)

        # 2. Update Canvas Backgrounds
        new_bg = THEME_COLORS[new_mode]["canvas_bg"]
        self.canvas_table.configure(bg=new_bg)
        self.canvas_tree.configure(bg=new_bg)

        # 3. Redraw content if available
        if self.last_tokens:
            self.draw_cyk_pyramid(self.last_table, self.last_tokens)
            self.draw_parse_tree(self.last_tree_structure, self.last_tokens)

        # Update switch text to reflect mode
        self.switch_theme.configure(text=f"{new_mode} Mode")

    def start_parsing(self):
        sentence = self.entry_sentence.get().strip()
        if not sentence:
            self.lbl_status.configure(text="Mohon masukkan kalimat bahasa Bali.", text_color="orange")
            return

        self.lbl_status.configure(text="Memproses...", text_color="gray")
        self.update()

        # Run CYK Algorithm
        is_valid, table, tokens = cyk_parse(sentence.lower(), self.grammar)

        # Store state for theme switching redraws
        self.last_table = table
        self.last_tokens = tokens
        self.last_tree_structure = get_parse_tree_structure(self.grammar, table, tokens) if is_valid else None

        # Update Visuals
        self.draw_cyk_pyramid(table, tokens)

        if is_valid:
            self.lbl_status.configure(text="✔ Kalimat Valid.", text_color="#2CC985") # Green
            self.draw_parse_tree(self.last_tree_structure, tokens)
        else:
            self.lbl_status.configure(text="✘ Kalimat Tidak Valid.", text_color="#E74C3C") # Red
            self.canvas_tree.delete("all")
            self.canvas_tree.create_text(
                self.canvas_tree.winfo_width() / 2, self.canvas_tree.winfo_height() / 2,
                text="Tidak ada pohon parse karena kalimat tidak valid.",
                fill=THEME_COLORS[self.current_theme_mode]["empty_text"],
                font=("Arial", 16)
            )

    def reset_app(self):
        self.entry_sentence.delete(0, 'end')
        self.lbl_status.configure(text="Menunggu input kalimat...", text_color="gray")
        self.canvas_table.delete("all")
        self.canvas_tree.delete("all")
        self.last_tree_structure = None
        self.last_table = None
        self.last_tokens = None

    def draw_cyk_pyramid(self, table, tokens):
        """
        Draws the CYK triangle table on the canvas.
        Adapted from the original code but styled for dark mode.
        """
        canvas = self.canvas_table
        canvas.delete("all")

        n = len(tokens)
        if n == 0: return

        # Get colors based on current theme
        theme = THEME_COLORS[self.current_theme_mode]

        # Configuration
        BOX_HEIGHT = 60
        START_X = 50
        # Calculate vertical position to center or start with margin
        # We start drawing from bottom to top
        BASE_Y = 50 + (n * BOX_HEIGHT)

        # Pre-calculation for column widths
        col_widths = []
        for i in range(n):
            max_char_len = len(tokens[i])
            for length in range(1, n - i + 1):
                j = i + length - 1
                if table[i][j]:
                    isi = ", ".join(sorted(list(table[i][j])))
                    max_char_len = max(max_char_len, len(isi))

            # Width calculation: Char length * font_estimate + padding
            calculated_width = max(80, (max_char_len * 10) + 30)
            col_widths.append(calculated_width)

        total_width = sum(col_widths) + 100
        total_height = (n * BOX_HEIGHT) + 150
        canvas.config(scrollregion=(0, 0, total_width, total_height))

        # Centering logic if the content is smaller than canvas
        canvas_width = canvas.winfo_width()
        start_x_offset = START_X
        if total_width < canvas_width:
             start_x_offset = (canvas_width - total_width) / 2 + START_X

        current_x = start_x_offset

        for i in range(n):
            this_col_width = col_widths[i]

            # Draw boxes upwards
            for length in range(1, n - i + 1):
                j = i + length - 1

                x1 = current_x
                x2 = current_x + this_col_width

                y2 = BASE_Y - ((length - 1) * BOX_HEIGHT)
                y1 = y2 - BOX_HEIGHT

                # Content
                if table[i][j]:
                    content_list = sorted(list(table[i][j]))
                    isi_teks = ", ".join(content_list)
                    # Highlight 'K' (Start Symbol)
                    text_color = theme["k_text"] if 'K' in content_list else theme["text"]
                    box_fill = theme["k_fill"] if 'K' in content_list else theme["box_fill"]
                else:
                    isi_teks = "-"
                    text_color = theme["empty_text"]
                    box_fill = theme["box_fill"]

                # Draw Rectangle
                canvas.create_rectangle(x1, y1, x2, y2, fill=box_fill, outline=theme["box_outline"], width=1)

                # Font size logic
                font_size = 10 if len(isi_teks) > 15 else 12

                canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2,
                    text=isi_teks, fill=text_color,
                    font=("Roboto", font_size, "bold" if 'K' in isi_teks else "normal")
                )

            # Draw Token at bottom
            y_text = BASE_Y + 30
            x_center = current_x + (this_col_width / 2)
            canvas.create_text(
                x_center, y_text,
                text=tokens[i], fill=theme["token"],
                font=("Roboto", 13, "italic", "bold")
            )

            current_x += this_col_width

    def draw_parse_tree(self, tree_structure, tokens):
        """
        Draws the parse tree on the canvas.
        Adapted from original recursive_draw logic.
        """
        canvas = self.canvas_tree
        canvas.delete("all")

        if not tree_structure:
            return

        # Get colors based on current theme
        theme = THEME_COLORS[self.current_theme_mode]

        X_SPACING = 120
        Y_SPACING = 90
        START_Y = 60

        # Calculate canvas size
        total_width = max(800, len(tokens) * X_SPACING + 100)
        total_height = max(600, (len(tokens) * 50) + 200)
        canvas.config(scrollregion=(0, 0, total_width, total_height))

        # Center horizontally if small
        canvas_width = self.canvas_tree.winfo_width()
        start_x_offset = 50
        if total_width < canvas_width:
             start_x_offset = (canvas_width - total_width) / 2 + 50

        # Mutable tracker for leaf position
        leaf_tracker = [0]

        def recursive_draw_node(node, current_y):
            label = node[0]
            my_x = 0

            # --- Case 1: Binary Branch ---
            if len(node) == 3:
                left_child = node[1]
                right_child = node[2]

                x_left = recursive_draw_node(left_child, current_y + Y_SPACING)
                x_right = recursive_draw_node(right_child, current_y + Y_SPACING)

                my_x = (x_left + x_right) / 2

                # Draw lines
                canvas.create_line(my_x, current_y + 20, x_left, current_y + Y_SPACING - 20, fill=theme["line"], width=2)
                canvas.create_line(my_x, current_y + 20, x_right, current_y + Y_SPACING - 20, fill=theme["line"], width=2)

            # --- Case 2: Leaf Node (Word) ---
            elif len(node) == 2 and isinstance(node[1], str):
                kata = node[1]
                my_x = start_x_offset + (leaf_tracker[0] * X_SPACING)
                leaf_tracker[0] += 1

                y_kata = current_y + 60
                canvas.create_line(my_x, current_y + 20, my_x, y_kata - 15, fill=theme["dash_line"], dash=(2, 2))

                # Draw word
                canvas.create_text(
                    my_x, y_kata,
                    text=kata, font=("Roboto", 12, "italic", "bold"),
                    fill=theme["token"]
                )

            # --- Case 3: Unary Branch ---
            elif len(node) == 2 and isinstance(node[1], tuple):
                child_node = node[1]
                x_child = recursive_draw_node(child_node, current_y + Y_SPACING)
                my_x = x_child

                canvas.create_line(my_x, current_y + 20, x_child, current_y + Y_SPACING - 20, fill=theme["line"], width=2)

            # --- Draw Node Circle/Oval ---
            text_len = len(label)
            radius_x = max(25, (text_len * 7) + 10)
            radius_y = 20

            canvas.create_oval(
                my_x - radius_x, current_y - radius_y,
                my_x + radius_x, current_y + radius_y,
                fill=theme["node_fill"],
                outline=theme["node_outline"],
                width=2
            )

            canvas.create_text(
                my_x, current_y,
                text=label, font=("Roboto", 11, "bold"), fill=theme["node_text"]
            )

            return my_x

        # Start drawing
        recursive_draw_node(tree_structure, START_Y)

if __name__ == "__main__":
    app = BaliParserApp()
    app.mainloop()
