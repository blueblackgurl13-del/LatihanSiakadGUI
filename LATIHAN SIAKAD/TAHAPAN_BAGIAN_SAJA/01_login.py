# POTONGAN KODE BAGIAN INI SAJA
# Ini adalah cuplikan untuk dipelajari/dipresentasikan, bukan file aplikasi mandiri.
# Versi aplikasi utuh ada di ../FINAL/final_siakad.py

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
