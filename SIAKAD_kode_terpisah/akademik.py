import tkinter as tk
from tkinter import ttk, messagebox
from config import *


class AkademikMixin:
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
