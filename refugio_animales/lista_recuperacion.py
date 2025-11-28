import tkinter as tk
from tkinter import ttk
from datos.datos_animales import animales, recargar_animales  # Importar recargar_animales


class ListaRecuperacion:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#F1BB81")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="Animales en Recuperación 🏥",
            font=("Arial", 18), bg="#F1BB81"
        ).pack(pady=20)

        # Filtros
        filtros_frame = tk.Frame(self.frame, bg="#F1BB81")
        filtros_frame.pack(pady=5)

        # Buscar por nombre
        tk.Label(filtros_frame, text="Buscar por nombre:", bg="#F1BB81").grid(row=0, column=0, padx=5)
        self.entry_busqueda = tk.Entry(filtros_frame)
        self.entry_busqueda.grid(row=0, column=1, padx=5)

        # Filtrar por especie
        tk.Label(filtros_frame, text="Por especie:", bg="#F1BB81").grid(row=0, column=2, padx=5)
        self.combo_especie = ttk.Combobox(filtros_frame, values=["Todos", "Perro", "Gato"], state="readonly")
        self.combo_especie.set("Todos")
        self.combo_especie.grid(row=0, column=3, padx=5)

        # Filtrar por estado de salud
        tk.Label(filtros_frame, text="Estado de salud:", bg="#F1BB81").grid(row=0, column=4, padx=5)
        self.combo_salud = ttk.Combobox(filtros_frame, values=["Todos", "Grave", "Regular"], state="readonly")
        self.combo_salud.set("Todos")
        self.combo_salud.grid(row=0, column=5, padx=5)

        # Botón aplicar
        tk.Button(filtros_frame, text="Aplicar Filtro", command=self.cargar_recuperacion).grid(row=0, column=6, padx=5)

        # Atajos: enter y selección directa
        self.entry_busqueda.bind("<Return>", lambda event: self.cargar_recuperacion())
        self.combo_especie.bind("<<ComboboxSelected>>", lambda event: self.cargar_recuperacion())
        self.combo_salud.bind("<<ComboboxSelected>>", lambda event: self.cargar_recuperacion())



        # Frame para la tabla
        frame_tabla = tk.Frame(self.frame, bg="#F1BB81")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("nombre", "especie", "raza", "edad", "salud")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        self.tree.pack(side="left", fill="both", expand=True)

        encabezados = {
            "nombre": "Nombre",
            "especie": "Especie",
            "raza": "Raza",
            "edad": "Edad",
            "salud": "Salud"
        }

        for col in columnas:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.cargar_recuperacion()

    def cargar_recuperacion(self):
        recargar_animales()

        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Obtener filtros (en minúsculas para comparación)
        nombre_filtro = self.entry_busqueda.get().strip().lower()
        especie_filtro = self.combo_especie.get().lower()
        estado_salud_filtro = self.combo_salud.get().lower()

        for animal in animales:
            salud = animal.get("salud", "").lower()
            especie = animal.get("especie", "").lower()
            nombre = animal.get("nombre", "").lower()

            # Solo mostrar animales con salud grave o regular
            if salud not in ["regular", "grave"]:
                continue

            # Aplicar filtro de nombre (si hay texto)
            if nombre_filtro and nombre_filtro not in nombre:
                continue

            # Aplicar filtro de especie (si no es "todos")
            if especie_filtro != "todos" and especie != especie_filtro:
                continue

            # Aplicar filtro de salud (si no es "todos")
            if estado_salud_filtro != "todos" and salud != estado_salud_filtro:
                continue

            # Mostrar en la tabla
            self.tree.insert("", "end", values=(
                animal.get("nombre"),
                animal.get("especie"),
                animal.get("raza"),
                animal.get("edad"),
                animal.get("salud")
            ))
