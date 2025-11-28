import tkinter as tk
from tkinter import ttk
from datos.datos_animales import animales, recargar_animales


class BuscarAnimal:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#F1BB81")

        tk.Label(master, text="Lista General de Animales 🐾", font=("Arial", 18), bg="#F1BB81").pack(pady=20)

        # Filtros
        filtros_frame = tk.Frame(master, bg="#F1BB81")
        filtros_frame.pack(pady=10)

        tk.Label(filtros_frame, text="Nombre:", bg="#F1BB81").grid(row=0, column=0, padx=5)
        self.entry_nombre = tk.Entry(filtros_frame)
        self.entry_nombre.grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Especie:", bg="#F1BB81").grid(row=0, column=2, padx=5)
        self.combo_especie = ttk.Combobox(filtros_frame, values=["Todos", "Perro", "Gato", "Otro"], state="readonly")
        self.combo_especie.set("Todos")
        self.combo_especie.grid(row=0, column=3, padx=5)

        tk.Label(filtros_frame, text="Raza:", bg="#F1BB81").grid(row=1, column=0, padx=5)
        self.entry_raza = tk.Entry(filtros_frame)
        self.entry_raza.grid(row=1, column=1, padx=5)

        tk.Label(filtros_frame, text="Edad:", bg="#F1BB81").grid(row=1, column=2, padx=5)
        self.entry_edad = tk.Entry(filtros_frame)
        self.entry_edad.grid(row=1, column=3, padx=5)

        tk.Label(filtros_frame, text="Estado de adopción:", bg="#F1BB81").grid(row=2, column=0, padx=5)
        self.combo_estado = ttk.Combobox(filtros_frame, values=["Todos", "Adoptado", "En Adopción"], state="readonly")
        self.combo_estado.set("Todos")
        self.combo_estado.grid(row=2, column=1, padx=5)

        tk.Label(filtros_frame, text="Salud:", bg="#F1BB81").grid(row=2, column=2, padx=5)
        self.combo_salud = ttk.Combobox(filtros_frame, values=["Todos", "Buena", "Regular", "Grave"], state="readonly")
        self.combo_salud.set("Todos")
        self.combo_salud.grid(row=2, column=3, padx=5)

        tk.Button(filtros_frame, text="Aplicar Filtros", command=self.buscar, bg="#C72213", fg="white").grid(row=3, column=0, columnspan=4, pady=10)

        # Tabla
        frame_resultados = tk.Frame(master, bg="#FFFFFF")
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("nombre", "especie", "raza", "edad", "salud", "estado_actual")
        self.tree = ttk.Treeview(frame_resultados, columns=columnas, show="headings", height=15)
        self.tree.pack(side="left", fill="both", expand=True)

        encabezados = {
            "nombre": "Nombre",
            "especie": "Especie",
            "raza": "Raza",
            "edad": "Edad",
            "salud": "Salud",
            "estado_actual": "Estado Actual"
        }

        for col in columnas:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Cargar al inicio
        self.buscar()

    def buscar(self):
        recargar_animales()
        self.tree.delete(*self.tree.get_children())

        nombre_filtro = self.entry_nombre.get().strip().lower()
        especie_filtro = self.combo_especie.get().lower()
        raza_filtro = self.entry_raza.get().strip().lower()
        edad_filtro = self.entry_edad.get().strip()
        estado_filtro = self.combo_estado.get().lower()
        salud_filtro = self.combo_salud.get().lower()

        for animal in sorted(animales, key=lambda x: x.get("nombre", "").lower()):
            if animal.get("estado_actual", "").lower() == "eliminado":
                continue

            nombre = animal.get("nombre", "").lower()
            especie = animal.get("especie", "").lower()
            raza = animal.get("raza", "").lower()
            edad = str(animal.get("edad", "")).strip()
            estado_actual = animal.get("estado_actual", "").lower()
            salud = animal.get("salud", "").lower()

            if nombre_filtro and nombre_filtro not in nombre:
                continue
            if especie_filtro != "todos" and especie != especie_filtro:
                continue
            if raza_filtro and raza_filtro not in raza:
                continue
            if edad_filtro and edad != edad_filtro:
                continue
            if estado_filtro != "todos" and estado_actual != estado_filtro:
                continue
            if salud_filtro != "todos" and salud != salud_filtro:
                continue

            self.tree.insert("", "end", values=(
                animal.get("nombre"),
                animal.get("especie"),
                animal.get("raza"),
                animal.get("edad"),
                animal.get("salud"),
                animal.get("estado_actual")
            ))
