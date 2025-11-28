import tkinter as tk
from tkinter import ttk
from datos.datos_animales import adopciones
from datos.datos_animales import guardar_datos, RUTA_ADOPCIONES, animales, RUTA_ANIMALES
from tkinter import messagebox


class ListaAdoptados:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#F1BB81")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="Animales Adoptados 🐕‍🦺🏠",
            font=("Arial", 18), bg="#F1BB81"
        ).pack(pady=10)

        # 🔍 Barra de búsqueda
        buscar_frame = tk.Frame(self.frame, bg="#F1BB81")
        buscar_frame.pack(pady=5)

        tk.Label(buscar_frame, text="Buscar:", bg="#F1BB81").pack(side="left", padx=5)
        self.buscar_var = tk.StringVar()
        buscar_entry = tk.Entry(buscar_frame, textvariable=self.buscar_var)
        buscar_entry.pack(side="left", padx=5)
        buscar_entry.bind("<KeyRelease>", self.filtrar_datos)

        # 🔽 Filtro por especie
        tk.Label(buscar_frame, text="Especie:", bg="#F1BB81").pack(side="left", padx=10)
        self.especie_var = tk.StringVar(value="Todas")
        especies = ["Todas"] + sorted(set(a["especie"] for a in adopciones))
        self.especie_combo = ttk.Combobox(buscar_frame, textvariable=self.especie_var, values=especies, state="readonly")
        self.especie_combo.pack(side="left", padx=5)
        self.especie_combo.bind("<<ComboboxSelected>>", self.filtrar_datos)

        # 🔄 Botón actualizar
        ttk.Button(buscar_frame, text="Actualizar", command=self.cargar_datos).pack(side="left", padx=10)

        # 🧾 Tabla
        columnas = (
            "Animal", "Especie", "Edad", "Salud",
            "Adoptante", "Correo", "Teléfono", "INE", "Notas", "Fecha"
        )
        self.tabla = ttk.Treeview(self.frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")

        self.tabla.pack(padx=20, pady=10, fill="both", expand=True)

        # Scroll horizontal si es necesario
        scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(fill="x")

        self.cargar_datos()

        #🗑️ Botón para eliminar adopción
        ttk.Button(self.frame, text="Eliminar Adopción", command=self.eliminar_adopcion).pack(pady=5)


    def eliminar_adopcion(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona una fila", "Por favor selecciona una adopción para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta adopción?")
        if not confirmacion:
            return

        item = self.tabla.item(seleccionado[0])
        valores = item["values"]
        nombre_animal = valores[0]
        adoptante = valores[4]

        # Eliminar adopción
        for i, adopcion in enumerate(adopciones):
            if adopcion["animal"] == nombre_animal and adopcion["adoptante"] == adoptante:
                del adopciones[i]
                break

        # 🧠 Guardar cambios en adopciones.json
        guardar_datos(RUTA_ADOPCIONES, adopciones)

        # 🐾 Restaurar estado del animal
        from datos.datos_animales import animales, RUTA_ANIMALES  # asegura datos actualizados
        for animal in animales:
            if animal.get("nombre") == nombre_animal:
                animal["estado_actual"] = "En Adopción"
                animal.pop("adoptante", None)  # Quitar datos del adoptante si existen
                break

        guardar_datos(RUTA_ANIMALES, animales)

        self.cargar_datos()
        messagebox.showinfo("Éxito", f"Adopción de '{nombre_animal}' eliminada y estado restaurado.")



    def cargar_datos(self):
        self.tabla.delete(*self.tabla.get_children())

        for adopcion in adopciones:
            self.tabla.insert(
                "", "end",
                values=(
                    adopcion.get("animal"),
                    adopcion.get("especie"),
                    adopcion.get("edad"),
                    adopcion.get("salud"),
                    adopcion.get("adoptante"),
                    adopcion.get("correo"),
                    adopcion.get("telefono"),
                    adopcion.get("ine"),
                    adopcion.get("notas", ""),
                    adopcion.get("fecha")
                )
            )

    def filtrar_datos(self, event=None):
        busqueda = self.buscar_var.get().lower()
        especie_filtro = self.especie_var.get()

        self.tabla.delete(*self.tabla.get_children())

        for adopcion in adopciones:
            if especie_filtro != "Todas" and adopcion.get("especie") != especie_filtro:
                continue

            texto_busqueda = (
                f"{adopcion.get('animal', '')} {adopcion.get('adoptante', '')}"
            ).lower()

            if busqueda in texto_busqueda:
                self.tabla.insert(
                    "", "end",
                    values=(
                        adopcion.get("animal"),
                        adopcion.get("especie"),
                        adopcion.get("edad"),
                        adopcion.get("salud"),
                        adopcion.get("adoptante"),
                        adopcion.get("correo"),
                        adopcion.get("telefono"),
                        adopcion.get("ine"),
                        adopcion.get("notas", ""),
                        adopcion.get("fecha")
                    )
                )
