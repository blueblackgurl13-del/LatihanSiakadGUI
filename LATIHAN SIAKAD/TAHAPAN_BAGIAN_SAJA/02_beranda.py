# POTONGAN KODE BAGIAN INI SAJA
# Ini adalah cuplikan untuk dipelajari/dipresentasikan, bukan file aplikasi mandiri.
# Versi aplikasi utuh ada di ../FINAL/final_siakad.py

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
