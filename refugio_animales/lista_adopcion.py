import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datos.datos_animales import animales, recargar_animales  # Importar recargar_animales


class ListaAdopcion:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#F1BB81")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Lista de Animales en Adopción 🏡",
                 font=("Arial", 18), bg="#F1BB81").pack(pady=10)

        # Filtros y búsqueda
        filtros_frame = tk.Frame(self.frame, bg="#F1BB81")
        filtros_frame.pack(pady=10)

        tk.Label(filtros_frame, text="Buscar nombre:", bg="#F1BB81").grid(row=0, column=0, padx=5)
        self.nombre_var = tk.StringVar()
        tk.Entry(filtros_frame, textvariable=self.nombre_var).grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Especie:", bg="#F1BB81").grid(row=0, column=2, padx=5)
        self.especie_var = tk.StringVar()
        especie_menu = ttk.Combobox(filtros_frame, textvariable=self.especie_var, values=["", "Perro", "Gato"], state="readonly", width=10)
        especie_menu.grid(row=0, column=3, padx=5)

        tk.Label(filtros_frame, text="Salud:", bg="#F1BB81").grid(row=0, column=4, padx=5)
        self.salud_var = tk.StringVar()
        salud_menu = ttk.Combobox(filtros_frame, textvariable=self.salud_var, values=["", "Buena", "Regular", "Grave"], state="readonly", width=10)
        salud_menu.grid(row=0, column=5, padx=5)

        tk.Button(filtros_frame, text="Aplicar filtros", command=self.cargar_datos, bg="#F5E72D", fg="black").grid(row=0, column=6, padx=10)
        tk.Button(filtros_frame, text="Limpiar", command=self.limpiar_filtros, bg="#213B9C", fg="white").grid(row=0, column=7, padx=5)

        # Tabla
        self.tabla = ttk.Treeview(self.frame, columns=("Nombre", "Especie", "Edad", "Salud"), show="headings", height=10)
        for col in ("Nombre", "Especie", "Edad", "Salud"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)
        self.tabla.pack(padx=20, pady=10, fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_imagen)

        # Imagen
        self.label_imagen = tk.Label(self.frame, bg="#F1BB81")
        self.label_imagen.pack(pady=10)

        self.imagen_actual = None  # mantener referencia para evitar recolección

        self.cargar_datos()

    def limpiar_filtros(self):
        self.nombre_var.set("")
        self.especie_var.set("")
        self.salud_var.set("")
        self.cargar_datos()

    def cargar_datos(self):
        recargar_animales()  # <-- recargar antes de cargar tabla

        for i in self.tabla.get_children():
            self.tabla.delete(i)

        nombre_filtro = self.nombre_var.get().lower()
        especie_filtro = self.especie_var.get()
        salud_filtro = self.salud_var.get()

        for animal in animales:
            if animal.get("estado_actual") != "En Adopción":
                continue

            if nombre_filtro and nombre_filtro not in animal.get("nombre", "").lower():
                continue
            if especie_filtro and especie_filtro != animal.get("especie"):
                continue
            if salud_filtro and salud_filtro != animal.get("salud"):
                continue

            self.tabla.insert(
                "", "end",
                values=(animal.get("nombre"), animal.get("especie"), animal.get("edad"), animal.get("salud")),
                tags=(animal.get("foto", ""),)
            )

        self.label_imagen.config(image="")

    def mostrar_imagen(self, event):
        selected = self.tabla.focus()
        if not selected:
            return

        foto_path = self.tabla.item(selected, "tags")[0]
        if not foto_path or not os.path.exists(foto_path):
            self.label_imagen.config(image="", text="Sin imagen disponible")
            return

        try:
            imagen = Image.open(foto_path)
            imagen = imagen.resize((180, 180))
            self.imagen_actual = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=self.imagen_actual, text="")
        except Exception as e:
            self.label_imagen.config(text="Error al cargar imagen", image="")
            print(f"Error al cargar imagen: {e}")
