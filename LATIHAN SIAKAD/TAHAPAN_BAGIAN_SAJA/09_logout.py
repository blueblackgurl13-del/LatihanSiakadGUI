# POTONGAN KODE BAGIAN INI SAJA
# Ini adalah cuplikan untuk dipelajari/dipresentasikan, bukan file aplikasi mandiri.
# Versi aplikasi utuh ada di ../FINAL/final_siakad.py

def logout(self):

        if messagebox.askyesno(

            "Logout", "Yakin ingin keluar dari SIAKAD?"

        ):

            self.user = None

            self.show_login()
