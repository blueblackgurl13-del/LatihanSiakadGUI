import tkinter as tk
from tkinter import ttk
from config import *
from database import get_connection


class CoreMixin:
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
