import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import os

class VentanaChat:
    def __init__(self, app, chat_name, volver):
        self.app = app
        self.chat_name = chat_name
        self.volver = volver
        self.historial_path = f"historial_{chat_name}.txt"
        self.imagenes_cargadas = []  # Para mantener referencia a imágenes y evitar que se eliminen por GC

    def mostrar(self):
        ctk.set_appearance_mode("dark" if self.app.modo_oscuro else "light")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title(f"{self.chat_name} - {self.app.nickname}")
        self.window.geometry("750x600")

        # Frame scrollable para mensajes
        self.frame_mensajes = ctk.CTkScrollableFrame(self.window, height=400)
        self.frame_mensajes.pack(padx=10, pady=10, fill="both", expand=True)

        # Entrada y botones en un frame
        frame_entrada = ctk.CTkFrame(self.window)
        frame_entrada.pack(padx=10, pady=(0,10), fill="x")

        self.entry = ctk.CTkEntry(frame_entrada, placeholder_text="Escribe un mensaje...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.entry.bind("<Return>", lambda e: self.enviar())

        ctk.CTkButton(frame_entrada, text="Enviar", command=self.enviar).pack(side="left", padx=5)
        ctk.CTkButton(frame_entrada, text="Adjuntar", command=self.adjuntar_archivo).pack(side="left", padx=5)
        ctk.CTkButton(frame_entrada, text="← Volver", command=self.salir).pack(side="left", padx=5)

        self.cargar_historial()

        self.window.mainloop()

    def agregar_mensaje(self, texto, es_imagen=False):
        hora = datetime.now().strftime("%I:%M %p")
        if es_imagen:
            # Mostrar la imagen
            img = Image.open(texto)
            max_width = 600
            max_height = 600
            img.thumbnail((max_width, max_height))
            img_tk = ctk.CTkImage(img)
            label_img = ctk.CTkLabel(self.frame_mensajes, image=img_tk)
            label_img.image = img_tk  # guardar referencia para evitar GC
            label_img.pack(anchor="w", pady=5)
            self.imagenes_cargadas.append(label_img)
            # Añadir texto con nombre y hora debajo o arriba
            label_info = ctk.CTkLabel(self.frame_mensajes, text=f"[{hora}] {self.app.nickname} envió una imagen")
            label_info.pack(anchor="w", pady=(0,5))
        else:
            # Texto normal
            label = ctk.CTkLabel(self.frame_mensajes, text=f"[{hora}] {texto}", wraplength=400, justify="left")
            label.pack(anchor="w", pady=2)

    def cargar_historial(self):
        if os.path.exists(self.historial_path):
            with open(self.historial_path, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            for linea in lineas:
                linea = linea.strip()
                if linea.startswith("[IMG]"):
                    ruta_img = linea[5:]
                    if os.path.exists(ruta_img):
                        self.agregar_mensaje(ruta_img, es_imagen=True)
                else:
                    self.agregar_mensaje(linea)

    def enviar(self):
        texto = self.entry.get().strip()
        if texto:
            mensaje_usuario = f"{self.app.nickname}: {texto}"
            self.agregar_mensaje(mensaje_usuario)
            self.entry.delete(0, "end")

            # Guardar en historial
            with open(self.historial_path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%I:%M %p')}] {mensaje_usuario}\n")

    def adjuntar_archivo(self):
        filepath = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")])
        if filepath:
            self.agregar_mensaje(filepath, es_imagen=True)

            # Guardar en historial con prefijo [IMG]
            with open(self.historial_path, "a", encoding="utf-8") as f:
                f.write(f"[IMG]{filepath}\n")

    def salir(self):
        self.window.destroy()
        self.volver(self.app).mostrar()
