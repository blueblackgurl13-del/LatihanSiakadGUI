import tkinter as tk

import os

from tkinter import ttk, messagebox

from database import get_connection, setup_login, check_login



# ==========================================
# KONFIGURASI APLIKASI - STITEK BONTANG
# ==========================================

BG = "#F3F6FB"
NAVY = "#101D3A"
BLUE = "#2463D4"
PURPLE = "#3979E8"
ORANGE = "#F28C28"
WHITE = "#FFFFFF"
TEXT = "#1D2A42"
MUTED = "#78859A"

PINK_LIGHT = "#EAF1FF"
PINK_PALE = "#F3F6FB"
LAVENDER = "#EAF0FC"
BLUE_LIGHT = "#EAF1FF"
SAGE = "#E7F3FF"
CREAM = "#FFF7ED"
PINK_BORDER = "#DDE5F0"
PINK_ACTIVE = "#D97706"
PINK_ROW = "#FFFFFF"
PINK_ALT = "#F4F7FC"
LILAC_ROW = "#F8FAFD"
FONT = "Segoe UI"
FONT_TITLE = ("Segoe UI", 23, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)


TABLES = {

    "Mahasiswa": ("mahasiswa", "nim"),

    "Dosen": ("dosen", "nip"),

    "Mata Kuliah": ("mata_kuliah", "kode_mk"),

    "KRS": ("krs", "id_krs"),

    "Jadwal Kuliah": ("jadwal_kuliah", "id_jadwal"),

    "Pembayaran UKT": ("pembayaran_ukt", "id_pembayaran"),

}





class SiakadApp:

    def __init__(self, root):

        self.root = root

        self.root.title("SIAKAD | STITEK Bontang")

        self.root.geometry("1200x720")

        self.root.minsize(950, 600)

        self.root.configure(bg=BG)



        self.user = None

        self.current_label = None

        self.columns = []

        self.tree = None

        self.nav_buttons = {}
        self.all_rows = []
        self.search_var = None
        self.dashboard_search_var = None



        self.setup_style()

        self.show_login()



    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")



        # Tabel lebih ringan, dengan baris lega dan header pastel.

        style.configure(

            "Treeview",

            background=PINK_ROW,

            foreground=TEXT,

            rowheight=38,

            fieldbackground=PINK_ROW,

            font=("Segoe UI", 10),

            borderwidth=0,

            relief="flat",

            padding=(4, 3)

        )

        style.configure(

            "Treeview.Heading",

            background="#EAF0FA",

            foreground="#1B3768",

            font=("Segoe UI", 9, "bold"),

            relief="flat",

            padding=(12, 12)

        )

        style.map(

            "Treeview",

            background=[("selected", "#D7E5FA")],

            foreground=[("selected", "#172554")]

        )

        style.map(

            "Treeview.Heading",

            background=[("active", "#DCE8FA")]

        )



        style.configure(

            "TEntry",

            padding=(10, 9),

            fieldbackground="#FFFFFF",

            foreground=TEXT,

            bordercolor="#DDE5F0",

            lightcolor="#DDE5F0",

            darkcolor="#DDE5F0"

        )

        style.map(

            "TEntry",

            bordercolor=[("focus", "#F28C28")],

            lightcolor=[("focus", "#F28C28")],

            darkcolor=[("focus", "#F28C28")]

        )

        style.configure(

            "Vertical.TScrollbar",

            background="#DDE5F0",

            troughcolor="#F3F6FA",

            bordercolor="#F3F6FA",

            arrowcolor="#52627A",

            relief="flat"

        )

        style.configure(

            "Horizontal.TScrollbar",

            background="#DDE5F0",

            troughcolor="#F3F6FA",

            bordercolor="#F3F6FA",

            arrowcolor="#52627A",

            relief="flat"

        )



    def clear(self):

        for widget in self.root.winfo_children():

            widget.destroy()



    # ==========================================

    # HALAMAN LOGIN

    # ==========================================



    def show_login(self):
        self.clear()
        self.root.configure(bg=WHITE)

        page = tk.Frame(self.root, bg=WHITE, highlightbackground="#DCE3ED", highlightthickness=1)
        page.pack(fill="both", expand=True, padx=12, pady=12)
        page.grid_columnconfigure(0, weight=11, uniform="login")
        page.grid_columnconfigure(1, weight=10, uniform="login")
        page.grid_rowconfigure(0, weight=1)

        # Panel identitas kampus
        left = tk.Frame(page, bg=NAVY, padx=42, pady=36)
        left.grid(row=0, column=0, sticky="nsew")
        tk.Frame(left, bg=ORANGE, height=4).pack(fill="x", pady=(0, 28))
        tk.Label(left, text="STITEK BONTANG", bg=NAVY, fg="#F6A64B",
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(0, 8))
        tk.Label(left, text="SISTEM INFORMASI\nAKADEMIK", bg=NAVY, fg=WHITE,
                 font=(FONT, 25, "bold"), justify="left").pack(anchor="w", pady=(0, 28))
        tk.Label(left, text="Pusat Layanan Akademik", bg="#1C2B4A", fg=WHITE,
                 font=(FONT, 10, "bold"), padx=14, pady=10).pack(anchor="w", pady=(0, 24))
        tk.Label(left, text="Kelola informasi akademik dalam satu platform yang\nterstruktur, aman, dan mudah digunakan.",
                 bg=NAVY, fg="#D5DDEC", font=(FONT, 13), justify="left", wraplength=440).pack(anchor="w", pady=(0, 28))

        features = tk.Frame(left, bg=NAVY)
        features.pack(fill="x", pady=(0, 20))
        for title, desc in [("Data Akademik", "Mahasiswa, dosen, dan mata kuliah"),
                            ("Layanan Terpadu", "KRS, jadwal kuliah, dan pembayaran UKT")]:
            box = tk.Frame(features, bg="#182641", padx=14, pady=13,
                           highlightbackground="#35425A", highlightthickness=1)
            box.pack(fill="x", pady=5)
            tk.Label(box, text=title, bg="#182641", fg=WHITE,
                     font=(FONT, 10, "bold")).pack(anchor="w")
            tk.Label(box, text=desc, bg="#182641", fg="#C5D0E0",
                     font=(FONT, 9)).pack(anchor="w", pady=(4, 0))
        tk.Label(left, text="STITEK Bontang  |  Sistem Informasi Akademik", bg=NAVY,
                 fg="#AEBBD0", font=(FONT, 9)).pack(side="bottom", anchor="w")

        # Panel login
        right = tk.Frame(page, bg=WHITE, padx=48, pady=38)
        right.grid(row=0, column=1, sticky="nsew")
        tk.Label(right, text="LOGIN", bg=WHITE, fg=BLUE,
                 font=(FONT, 10, "bold")).pack(anchor="w", pady=(28, 12))
        tk.Label(right, text="Masuk ke akun Anda", bg=WHITE, fg=NAVY,
                 font=(FONT, 25, "bold")).pack(anchor="w")
        tk.Label(right, text="Gunakan username dan password yang terdaftar untuk\nmengakses layanan akademik kampus.",
                 bg=WHITE, fg=MUTED, font=(FONT, 10), justify="left").pack(anchor="w", pady=(12, 30))
        form = tk.Frame(right, bg=WHITE)
        form.pack(fill="x")
        tk.Label(form, text="Username", bg=WHITE, fg=TEXT,
                 font=(FONT, 10, "bold")).pack(anchor="w")
        self.username = ttk.Entry(form, font=(FONT, 11))
        self.username.pack(fill="x", ipady=7, pady=(7, 20))
        tk.Label(form, text="Password", bg=WHITE, fg=TEXT,
                 font=(FONT, 10, "bold")).pack(anchor="w")
        self.password = ttk.Entry(form, show="*", font=(FONT, 11))
        self.password.pack(fill="x", ipady=7, pady=(7, 24))
        self.password.bind("<Return>", lambda event: self.login())
        tk.Button(form, text="MASUK KE SIAKAD", command=self.login,
                  bg=ORANGE, fg=WHITE, activebackground="#D97706", activeforeground=WHITE,
                  relief="flat", cursor="hand2", font=(FONT, 10, "bold"), pady=13, bd=0).pack(fill="x")
        help_box = tk.Frame(right, bg="#F5F7FB", padx=14, pady=13,
                            highlightbackground="#E1E7F0", highlightthickness=1)
        help_box.pack(fill="x", pady=(28, 0))
        tk.Label(help_box, text="BANTUAN AKSES", bg="#F5F7FB", fg=NAVY,
                 font=(FONT, 9, "bold")).pack(anchor="w")
        tk.Label(help_box, text="Jika mengalami kendala login, hubungi administrator sistem kampus.",
                 bg="#F5F7FB", fg=MUTED, font=(FONT, 9), wraplength=380, justify="left").pack(anchor="w", pady=(7, 0))
        self.username.focus_set()

    def login(self):

        username = self.username.get().strip()

        password = self.password.get()



        if not username or not password:

            messagebox.showwarning(

                "Login", "Username dan password harus diisi."

            )

            return



        try:

            user = check_login(username, password)

            if user:

                self.user = user

                self.show_dashboard()

            else:

                messagebox.showerror(

                    "Login gagal",

                    "Username atau password salah."

                )

        except Exception as error:

            messagebox.showerror(

                "Koneksi database",

                f"Tidak bisa mengakses MySQL.\n\n{error}\n\n"

                "Pastikan MySQL aktif dan database siakad sudah diimport."

            )



    # ==========================================

    # DASHBOARD DENGAN MENU NAVIGASI DI ATAS

    # ==========================================



    def show_dashboard(self):
        """Dashboard dengan navigasi horizontal di bagian atas."""
        self.clear()
        self.root.configure(bg=BG)

        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)

        # Header / taskbar atas
        topbar = tk.Frame(
            shell, bg=WHITE, height=76,
            highlightbackground=PINK_BORDER, highlightthickness=1
        )
        topbar.pack(fill="x", padx=14, pady=(12, 0))
        topbar.pack_propagate(False)

        brand = tk.Frame(topbar, bg=WHITE)
        brand.pack(side="left", padx=(20, 18), pady=8)
        tk.Label(
            brand, text="STITEK BONTANG", bg=WHITE, fg=NAVY,
            font=(FONT, 12, "bold")
        ).pack(anchor="w")
        tk.Label(
            brand, text="SISTEM INFORMASI AKADEMIK", bg=WHITE, fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(anchor="w", pady=(3, 0))

        # Menu berada di atas, bukan sidebar kiri.
        nav_area = tk.Frame(topbar, bg=WHITE)
        nav_area.pack(side="left", fill="y", expand=True, padx=5, pady=13)
        self.nav_buttons = {}
        self.add_nav(nav_area, "Dashboard", self.show_home)
        for label in TABLES:
            self.add_nav(nav_area, label, lambda item=label: self.show_table(item))

        user_name = self.user.get("nama", "Pengguna") if isinstance(self.user, dict) else "Pengguna"
        user_area = tk.Frame(topbar, bg=WHITE)
        user_area.pack(side="right", padx=18, pady=8)
        tk.Label(
            user_area, text=user_name, bg=WHITE, fg=NAVY,
            font=(FONT, 9, "bold"), wraplength=130
        ).pack(anchor="e")
        tk.Button(
            user_area, text="Logout", command=self.logout,
            bg="#FFF1F0", fg="#B42332", activebackground="#FCE0DE",
            relief="flat", bd=0, padx=12, pady=5,
            font=(FONT, 8, "bold"), cursor="hand2"
        ).pack(anchor="e", pady=(4, 0))

        # Area konten dapat di-scroll agar seluruh beranda/modul terlihat.
        content_area = tk.Frame(shell, bg=BG)
        content_area.pack(fill="both", expand=True, padx=14, pady=(14, 10))
        self.content_canvas = tk.Canvas(content_area, bg=BG, highlightthickness=0, bd=0)
        self.content_scrollbar = ttk.Scrollbar(
            content_area, orient="vertical", command=self.content_canvas.yview
        )
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.content_scrollbar.pack(side="right", fill="y")
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content = tk.Frame(self.content_canvas, bg=BG)
        self.content_window = self.content_canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )
        self.content.bind(
            "<Configure>",
            lambda event: self.content_canvas.configure(
                scrollregion=self.content_canvas.bbox("all")
            )
        )
        self.content_canvas.bind(
            "<Configure>",
            lambda event: self.content_canvas.itemconfigure(
                self.content_window, width=event.width
            )
        )
        self.content_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.content_canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.content_canvas.bind_all("<Button-5>", self._on_mousewheel_linux)
        self.show_home()

    def _on_mousewheel(self, event):
        if not hasattr(self, "content_canvas") or not self.content_canvas.winfo_exists():
            return
        # Biarkan roda mouse menggulir tabelnya sendiri jika pointer di Treeview.
        if self.tree is not None and self.tree.winfo_exists():
            if str(event.widget).startswith(str(self.tree)):
                return
        try:
            if event.widget.winfo_toplevel() is not self.root:
                return
        except tk.TclError:
            return
        self.content_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if not hasattr(self, "content_canvas") or not self.content_canvas.winfo_exists():
            return
        if self.tree is not None and self.tree.winfo_exists():
            if str(event.widget).startswith(str(self.tree)):
                return
        try:
            if event.widget.winfo_toplevel() is not self.root:
                return
        except tk.TclError:
            return
        self.content_canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    def add_nav(self, parent, label, command):
        btn = tk.Button(
            parent, text=label, command=command,
            bg="#EAF1FF" if label == "Dashboard" else WHITE,
            fg=BLUE if label == "Dashboard" else "#53627A",
            activebackground="#EAF1FF", activeforeground=BLUE,
            relief="flat", bd=0, padx=10, pady=10,
            font=(FONT, 9, "bold" if label == "Dashboard" else "normal"),
            cursor="hand2"
        )
        btn.pack(side="left", padx=2, pady=2)
        self.nav_buttons[label] = btn

    def set_active(self, label):
        for name, btn in self.nav_buttons.items():
            active = name == label
            btn.configure(
                bg="#EAF1FF" if active else WHITE,
                fg=BLUE if active else "#53627A",
                font=(FONT, 9, "bold" if active else "normal")
            )

    def clear_content(self):

        for widget in self.content.winfo_children():

            widget.destroy()



    # ==========================================

    # FUNGSI DATABASE

    # ==========================================



    def run_query(self, sql, params=(), fetch=True):

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        try:

            cursor.execute(sql, params)

            result = cursor.fetchall() if fetch else None

            conn.commit()

            return result

        finally:

            cursor.close()

            conn.close()



    def get_columns(self, table):

        return self.run_query(

            """

            SELECT COLUMN_NAME, EXTRA, IS_NULLABLE,

                   COLUMN_DEFAULT, COLUMN_KEY, DATA_TYPE

            FROM INFORMATION_SCHEMA.COLUMNS

            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s

            ORDER BY ORDINAL_POSITION

            """,

            ("siakad", table)

        )



    # ==========================================

    # DASHBOARD UTAMA

    # ==========================================



    def show_home(self):
        self.clear_content()
        self.set_active("Dashboard")
        tk.Label(self.content, text="Dashboard", bg=BG, fg=NAVY,
                 font=(FONT, 24, "bold")).pack(anchor="w")
        tk.Label(self.content, text="Ringkasan data akademik STITEK Bontang.",
                 bg=BG, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(5, 20))

        name = self.user.get("nama", "Pengguna") if isinstance(self.user, dict) else "Pengguna"
        banner = tk.Frame(self.content, bg=NAVY, padx=24, pady=20)
        banner.pack(fill="x", pady=(0, 22))
        tk.Label(banner, text=f"Selamat datang, {name}", bg=NAVY, fg=WHITE,
                 font=(FONT, 17, "bold")).pack(anchor="w")
        tk.Label(banner, text="Kelola data akademik melalui menu navigasi di bagian atas.",
                 bg=NAVY, fg="#D8E1F0", font=(FONT, 10)).pack(anchor="w", pady=(6, 0))
        tk.Frame(banner, bg=ORANGE, height=4, width=68).pack(anchor="w", pady=(15, 0))

        search_row = tk.Frame(self.content, bg=BG)
        search_row.pack(fill="x", pady=(0, 16))
        tk.Label(search_row, text="Cari modul", bg=BG, fg=NAVY,
                 font=(FONT, 10, "bold")).pack(side="left", padx=(0, 10))
        self.dashboard_search_var = tk.StringVar()
        dashboard_search = ttk.Entry(search_row, textvariable=self.dashboard_search_var,
                                     font=(FONT, 10), width=34)
        dashboard_search.pack(side="left", ipady=4)

        tk.Label(self.content, text="Ringkasan Data", bg=BG, fg=NAVY,
                 font=(FONT, 13, "bold")).pack(anchor="w", pady=(0, 10))
        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 24))
        summary = [("Mahasiswa", "mahasiswa", BLUE), ("Dosen", "dosen", ORANGE),
                   ("Mata Kuliah", "mata_kuliah", "#39856B"), ("Pembayaran UKT", "pembayaran_ukt", "#7356B5")]
        for i, (label, table, accent) in enumerate(summary):
            card = tk.Frame(cards, bg=WHITE, highlightbackground=PINK_BORDER, highlightthickness=1, padx=17, pady=16, bd=0, relief="flat")
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 9, 0))
            cards.columnconfigure(i, weight=1, uniform="summary")
            tk.Frame(card, bg=accent, height=4).pack(fill="x", pady=(0, 13))
            tk.Label(card, text=label, bg=WHITE, fg=MUTED, font=(FONT, 9, "bold")).pack(anchor="w")
            try:
                total = self.run_query(f"SELECT COUNT(*) AS total FROM `{table}`")[0]["total"]
            except Exception:
                total = "—"
            tk.Label(card, text=str(total), bg=WHITE, fg=NAVY, font=(FONT, 25, "bold")).pack(anchor="w", pady=(8, 2))
            tk.Label(card, text="Total data tersimpan", bg=WHITE, fg=MUTED, font=(FONT, 8)).pack(anchor="w")

        tk.Label(self.content, text="Akses Modul", bg=BG, fg=NAVY,
                 font=(FONT, 13, "bold")).pack(anchor="w", pady=(0, 10))
        modules = tk.Frame(self.content, bg=BG)
        modules.pack(fill="x")

        def render_modules(*_):
            for child in modules.winfo_children():
                child.destroy()
            query = self.dashboard_search_var.get().strip().casefold()
            visible = [item for item in TABLES if query in item.casefold()]
            if not visible:
                tk.Label(modules, text="Modul tidak ditemukan.", bg=BG, fg=MUTED,
                         font=(FONT, 10)).grid(row=0, column=0, sticky="w", pady=10)
                return
            for i, label in enumerate(visible):
                card = tk.Frame(modules, bg=WHITE, highlightbackground=PINK_BORDER, highlightthickness=1)
                card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=(0 if i % 3 == 0 else 10, 0), pady=5)
                modules.columnconfigure(i % 3, weight=1, uniform="modules")
                tk.Label(card, text=label, bg=WHITE, fg=NAVY, font=(FONT, 11, "bold")).pack(anchor="w", padx=16, pady=(14, 4))
                tk.Label(card, text="Buka dan kelola data", bg=WHITE, fg=MUTED, font=(FONT, 9)).pack(anchor="w", padx=16)
                tk.Button(card, text="Buka modul  →", command=lambda item=label: self.show_table(item),
                          bg=WHITE, fg=BLUE, activebackground="#EAF1FF", relief="flat", bd=0,
                          font=(FONT, 9, "bold"), cursor="hand2").pack(anchor="w", padx=12, pady=(8, 12))

        self.dashboard_search_var.trace_add("write", render_modules)
        render_modules()

    def show_table(self, label):

        self.clear_content()

        self.current_label = label

        self.set_active(label)



        table, pk = TABLES[label]



        tk.Label(

            self.content, text=label,

            bg=BG, fg=NAVY,

            font=("Segoe UI", 22, "bold")

        ).pack(anchor="w")



        tk.Label(

            self.content, text=f"Data dari tabel {table}",

            bg=BG, fg=MUTED,

            font=("Segoe UI", 10)

        ).pack(anchor="w", pady=(3, 13))



        toolbar = tk.Frame(self.content, bg=BG)

        toolbar.pack(fill="x", pady=(0, 12))

        tk.Label(toolbar, text="Cari data:", bg=BG, fg=MUTED,
                 font=(FONT, 9, "bold")).pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=24,
                                 font=(FONT, 9))
        search_entry.pack(side="left", ipady=3, padx=(0, 10))
        self.search_var.trace_add("write", lambda *_: self.filter_table_rows())



        self.make_button(

            toolbar, "+  Tambah", self.add_record, "#F28C28", WHITE

        ).pack(side="left", padx=(0, 7))



        self.make_button(

            toolbar, "Edit", self.edit_record, "#EEF2FF", "#755F86"

        ).pack(side="left", padx=7)



        self.make_button(

            toolbar, "Hapus", self.delete_record, "#FDECEC", "#B42332"

        ).pack(side="left", padx=7)



        self.make_button(

            toolbar, "Refresh",

            lambda: self.load_table(label),

            "#FFFFFF", "#52627A"

        ).pack(side="right")



        frame = tk.Frame(

            self.content, bg=WHITE,

            highlightbackground=PINK_BORDER,

            highlightthickness=1

        )

        frame.pack(fill="both", expand=True)



        self.tree = ttk.Treeview(

            frame, show="headings", selectmode="browse"

        )



        yscroll = ttk.Scrollbar(

            frame, orient="vertical", command=self.tree.yview

        )

        xscroll = ttk.Scrollbar(

            frame, orient="horizontal", command=self.tree.xview

        )



        self.tree.configure(

            yscrollcommand=yscroll.set,

            xscrollcommand=xscroll.set

        )



        self.tree.grid(

            row=0, column=0, sticky="nsew",

            padx=(9, 0), pady=(9, 0)

        )

        yscroll.grid(row=0, column=1, sticky="ns", pady=(9, 0))

        xscroll.grid(

            row=1, column=0, sticky="ew",

            padx=(9, 0), pady=(0, 9)

        )



        frame.rowconfigure(0, weight=1)

        frame.columnconfigure(0, weight=1)



        self.load_table(label)



    def make_button(self, parent, text, command, bg, fg):

        return tk.Button(

            parent, text=text, command=command,

            bg=bg, fg=fg,

            activebackground=bg,

            activeforeground=fg,

            relief="flat",

            padx=14, pady=8,

            font=("Segoe UI", 9, "bold"),

            cursor="hand2"

        )



    def load_table(self, label):

        table, pk = TABLES[label]

        try:

            rows = self.run_query(f"SELECT * FROM `{table}`")

            info = self.get_columns(table)

            self.columns = [item["COLUMN_NAME"] for item in info]



            self.tree.delete(*self.tree.get_children())

            self.tree["columns"] = self.columns



            for col in self.columns:

                self.tree.heading(

                    col, text=col.replace("_", " ").title()

                )

                self.tree.column(

                    col,

                    width=max(110, min(190, len(col) * 11)),

                    minwidth=90,

                    anchor="w"

                )



            # Simpan semua data agar pencarian tidak perlu query ulang.
            self.all_rows = rows
            self.tree.tag_configure("odd", background="#FFFFFF")
            self.tree.tag_configure("even", background="#F4F7FB")
            if self.search_var is not None:
                self.search_var.set("")
            self.filter_table_rows()

        except Exception as error:

            messagebox.showerror("Gagal memuat data", str(error))



    # ==========================================

    def filter_table_rows(self):
        """Cari teks di seluruh kolom tabel yang sedang dibuka."""
        if self.tree is None or not self.tree.winfo_exists():
            return
        query = self.search_var.get().strip().casefold() if self.search_var is not None else ""
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for row in self.all_rows:
            values = ["" if row.get(col) is None else str(row.get(col)) for col in self.columns]
            if query and not any(query in value.casefold() for value in values):
                continue
            tag = "even" if shown % 2 else "odd"
            self.tree.insert("", "end", values=values, tags=(tag,))
            shown += 1

    # FORM TAMBAH DAN EDIT

    # ==========================================



    def selected_row(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(

                "Pilih data",

                "Pilih satu baris pada tabel terlebih dahulu."

            )

            return None



        return dict(zip(

            self.columns,

            self.tree.item(selected[0], "values")

        ))



    def record_form(self, title, fields, initial=None, readonly=None):

        initial = initial or {}

        readonly = set(readonly or [])

        result = {}



        win = tk.Toplevel(self.root)

        win.title(title)

        win.geometry("540x620")

        win.minsize(440, 350)

        win.configure(bg="#FFFFFF")

        win.transient(self.root)

        win.grab_set()



        tk.Label(

            win, text=title,

            bg="#FFFFFF", fg=NAVY,

            font=("Segoe UI", 15, "bold")

        ).pack(anchor="w", padx=20, pady=(18, 10))



        canvas = tk.Canvas(win, bg="#FFFFFF", highlightthickness=0)

        scrollbar = ttk.Scrollbar(

            win, orient="vertical", command=canvas.yview

        )

        inner = tk.Frame(canvas, bg="#FFFFFF")



        window_id = canvas.create_window(

            (0, 0), window=inner, anchor="nw"

        )



        inner.bind(

            "<Configure>",

            lambda event: canvas.configure(

                scrollregion=canvas.bbox("all")

            )

        )

        canvas.bind(

            "<Configure>",

            lambda event: canvas.itemconfigure(

                window_id, width=event.width

            )

        )

        canvas.configure(yscrollcommand=scrollbar.set)



        canvas.pack(side="left", fill="both", expand=True, padx=(18, 0))

        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=8)



        widgets = {}



        for field in fields:

            col = field["COLUMN_NAME"]



            # Kolom AUTO_INCREMENT diisi otomatis oleh MySQL.

            if "auto_increment" in (field["EXTRA"] or "").lower():

                continue



            tk.Label(

                inner,

                text=col.replace("_", " ").title(),

                bg="#FFFFFF", fg="#52627A",

                font=("Segoe UI", 9, "bold")

            ).pack(anchor="w", padx=4, pady=(7, 2))



            entry = ttk.Entry(inner, font=("Segoe UI", 10))

            entry.pack(fill="x", padx=4, ipady=5, pady=(0, 5))



            value = initial.get(col, "")

            if value is not None:

                entry.insert(0, str(value))



            if col in readonly:

                entry.configure(state="readonly")



            widgets[col] = entry



        def save():

            for col, entry in widgets.items():

                result[col] = entry.get().strip()

            win.destroy()



        tk.Button(

            win, text="Simpan Perubahan",

            command=save,

            bg=BLUE, fg=WHITE,

            activebackground=PINK_ACTIVE,

            activeforeground=WHITE,

            relief="flat", padx=20, pady=9,

            font=("Segoe UI", 10, "bold"),

            cursor="hand2"

        ).pack(pady=12)



        self.root.wait_window(win)

        return result if result else None



    def add_record(self):

        label = self.current_label

        table, pk = TABLES[label]



        try:

            fields = self.get_columns(table)

            values = self.record_form("Tambah " + label, fields)

            if values is None:

                return



            data = {}

            for field in fields:

                col = field["COLUMN_NAME"]

                if col not in values:

                    continue



                value = values[col]

                if value == "":

                    if (

                        field["IS_NULLABLE"] == "YES"

                        or field["COLUMN_DEFAULT"] is not None

                    ):

                        data[col] = None

                    else:

                        data[col] = value

                else:

                    data[col] = value



            if not data:

                return



            cols = list(data.keys())

            sql = (

                f"INSERT INTO `{table}` "

                f"({', '.join('`' + col + '`' for col in cols)}) "

                f"VALUES ({', '.join(['%s'] * len(cols))})"

            )



            self.run_query(

                sql, tuple(data[col] for col in cols), fetch=False

            )

            self.load_table(label)

            messagebox.showinfo("Berhasil", "Data berhasil ditambahkan.")



        except Exception as error:

            messagebox.showerror(

                "Gagal menambah data",

                f"Periksa input dan hubungan foreign key.\n\n{error}"

            )



    def edit_record(self):

        row = self.selected_row()

        if row is None:

            return



        label = self.current_label

        table, pk = TABLES[label]



        try:

            fields = self.get_columns(table)

            values = self.record_form(

                "Edit " + label,

                fields,

                initial=row,

                readonly=[pk]

            )

            if values is None:

                return



            update_cols = [

                field["COLUMN_NAME"]

                for field in fields

                if field["COLUMN_NAME"] != pk

                and field["COLUMN_NAME"] in values

            ]

            if not update_cols:

                return



            assignments = ", ".join(

                f"`{col}`=%s" for col in update_cols

            )

            params = [

                values[col] if values[col] != "" else None

                for col in update_cols

            ]

            params.append(row[pk])



            self.run_query(

                f"UPDATE `{table}` SET {assignments} WHERE `{pk}`=%s",

                tuple(params),

                fetch=False

            )

            self.load_table(label)

            messagebox.showinfo("Berhasil", "Data berhasil diperbarui.")



        except Exception as error:

            messagebox.showerror(

                "Gagal mengedit data",

                f"Periksa input dan hubungan foreign key.\n\n{error}"

            )



    def delete_record(self):

        row = self.selected_row()

        if row is None:

            return



        label = self.current_label

        table, pk = TABLES[label]



        yakin = messagebox.askyesno(

            "Konfirmasi hapus",

            f"Hapus data dengan {pk} = {row[pk]}?\n\n"

            "Data yang masih digunakan tabel lain mungkin tidak dapat dihapus."

        )

        if not yakin:

            return



        try:

            self.run_query(

                f"DELETE FROM `{table}` WHERE `{pk}`=%s",

                (row[pk],),

                fetch=False

            )

            self.load_table(label)

            messagebox.showinfo("Berhasil", "Data berhasil dihapus.")



        except Exception as error:

            messagebox.showerror(

                "Gagal menghapus data",

                f"Data mungkin masih digunakan oleh tabel lain.\n\n{error}"

            )



    # ==========================================

    # LOGOUT

    # ==========================================



    def logout(self):

        if messagebox.askyesno(

            "Logout", "Yakin ingin keluar dari SIAKAD?"

        ):

            self.user = None

            self.show_login()







if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()



    # ==========================================

    # IKON APLIKASI SIAKAD

    # ==========================================

    folder = os.path.dirname(os.path.abspath(__file__))

    lokasi_logo = os.path.join(folder, "stitek.jpg")



    try:

        logo = tk.PhotoImage(file=lokasi_logo)

        root.iconphoto(True, logo)

    except tk.TclError as error:

        print(f"Logo gagal dimuat: {error}")



    # ==========================================

    # JALANKAN APLIKASI

    # ==========================================

    try:

        setup_login()

        root.deiconify()



        app = SiakadApp(root)

        root.mainloop()



    except Exception as error:

        messagebox.showerror(

            "Kesalahan aplikasi",

            "Tidak dapat terhubung atau menyiapkan database.\n\n"

            f"{error}\n\n"

            "Pastikan MySQL XAMPP aktif, database siakad "

            "sudah diimport, dan pengaturan database.py benar."

        )

        root.destroy()