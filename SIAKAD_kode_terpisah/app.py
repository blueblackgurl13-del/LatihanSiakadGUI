"""Entry point utama SIAKAD STITEK Bontang."""
import os
import tkinter as tk
from tkinter import messagebox
from config import BG, WHITE
from core import CoreMixin
from login import LoginMixin
from dashboard import DashboardMixin
from akademik import AkademikMixin
from logout import LogoutMixin

class SiakadApp(CoreMixin, LoginMixin, DashboardMixin, AkademikMixin, LogoutMixin):
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

def main():
    root = tk.Tk()
    root.withdraw()
    folder = os.path.dirname(os.path.abspath(__file__))
    lokasi_logo = os.path.join(folder, "stitek.jpg")
    try:
        logo = tk.PhotoImage(file=lokasi_logo)
        root.iconphoto(True, logo)
    except tk.TclError as error:
        print(f"Logo gagal dimuat: {error}")
    try:
        from database import setup_login
        setup_login()
        root.deiconify()
        app = SiakadApp(root)
        root.mainloop()
    except Exception as error:
        messagebox.showerror(
            "Kesalahan aplikasi",
            "Tidak dapat terhubung atau menyiapkan database.\\n\\n"
            f"{error}\\n\\n"
            "Pastikan MySQL XAMPP aktif, database siakad sudah diimport, "
            "dan pengaturan database.py benar."
        )
        root.destroy()

if __name__ == "__main__":
    main()
