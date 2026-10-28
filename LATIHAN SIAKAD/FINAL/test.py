import tkinter as tk
import os

layar = tk.Tk()
layar.title("SIAKAD | Teknik Informatika")

folder = os.path.dirname(os.path.abspath(__file__))
lokasi_logo = os.path.join(folder, "love.png")

logo = tk.PhotoImage(file=lokasi_logo)
layar.iconphoto(True, logo)

layar.mainloop()