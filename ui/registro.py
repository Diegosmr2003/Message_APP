import customtkinter as ctk
from tkinter import messagebox
from ui.menu_principal import MenuPrincipal

class RegistroVentana:
    def __init__(self, app):
        self.app = app

    def mostrar(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Registro de Usuario")
        self.window.geometry("300x200")

        ctk.CTkLabel(self.window, text="Nombre:").pack(pady=(10, 0))
        self.entry_nombre = ctk.CTkEntry(self.window)
        self.entry_nombre.pack(pady=(0, 10))

        ctk.CTkLabel(self.window, text="Nickname:").pack()
        self.entry_nick = ctk.CTkEntry(self.window)
        self.entry_nick.pack(pady=(0, 10))

        ctk.CTkButton(self.window, text="Registrar", command=self.registrar).pack(pady=10)

        self.window.mainloop()

    def registrar(self):
        nombre = self.entry_nombre.get().strip()
        nick = self.entry_nick.get().strip()
        if nombre and nick:
            self.app.set_usuario(nombre, nick)
            self.window.destroy()
            MenuPrincipal(self.app).mostrar()
        else:
            messagebox.showwarning("Datos incompletos", "Por favor, ingresa nombre y nickname.")
