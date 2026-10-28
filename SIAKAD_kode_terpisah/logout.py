from tkinter import messagebox


class LogoutMixin:
    def logout(self):

        if messagebox.askyesno(

            "Logout", "Yakin ingin keluar dari SIAKAD?"

        ):

            self.user = None

            self.show_login()
