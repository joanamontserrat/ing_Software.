import tkinter as tk
from tkinter import ttk, messagebox
from datos.datos_animales import animales, guardar_datos, RUTA_ANIMALES
from datos.datos_animales import animales, guardar_datos, RUTA_ANIMALES, recargar_animales

class EditarEliminarAnimales:
    def __init__(self, master):
        self.master = master
        self.seleccionado = None

        recargar_animales()

        tk.Label(master, text="Editar o Eliminar Animales 🐾", font=("Arial", 18), bg="#F1BB81").pack(pady=20)

        # Filtros
        filtro_frame = tk.Frame(master, bg="#F1BB81")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="Buscar por nombre:", bg="#F1BB81").grid(row=0, column=0, padx=5)
        self.filtro_nombre = tk.Entry(filtro_frame)
        self.filtro_nombre.grid(row=0, column=1, padx=5)

        tk.Label(filtro_frame, text="Especie:", bg="#F1BB81").grid(row=0, column=2, padx=5)
        self.filtro_especie = ttk.Combobox(filtro_frame, values=["", "Perro", "Gato", "Otro"], state="readonly")
        self.filtro_especie.grid(row=0, column=3, padx=5)

        tk.Label(filtro_frame, text="Estado:", bg="#F1BB81").grid(row=0, column=4, padx=5)
        self.filtro_estado = ttk.Combobox(filtro_frame, values=["", "En Adopción", "Adoptado", "Recuperación"], state="readonly")
        self.filtro_estado.grid(row=0, column=5, padx=5)

        tk.Button(filtro_frame, text="Buscar", command=self.aplicar_filtros, bg="#F5E72D", fg="black").grid(row=0, column=6, padx=5)
        tk.Button(filtro_frame, text="Limpiar Filtros", command=self.limpiar_filtros, bg="#213B9C", fg="white").grid(row=0, column=7, padx=5)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("nombre", "especie", "raza", "edad", "salud", "estado_actual"), show="headings", height=10)
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        for col in ("nombre", "especie", "raza", "edad", "salud", "estado_actual"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_animal)

        # Formulario
        self.form_frame = tk.Frame(master, bg="#F1BB81")
        self.form_frame.pack(pady=10)

        self.campos = {
            "nombre": tk.Entry(self.form_frame),
            "especie": ttk.Combobox(self.form_frame, values=["Perro", "Gato", "Otro"]),
            "raza": tk.Entry(self.form_frame),
            "edad": tk.Entry(self.form_frame),
            "salud": ttk.Combobox(self.form_frame, values=["Bueno", "Regular", "Grave"]),
            "estado_actual": ttk.Combobox(self.form_frame, values=["En Adopción", "Adoptado", "Recuperación"])
        }

        for i, (clave, widget) in enumerate(self.campos.items()):
            tk.Label(self.form_frame, text=clave.capitalize() + ":", bg="#F1BB81", font=("Arial", 11))\
                .grid(row=i, column=0, sticky="e", padx=5, pady=5)
            widget.grid(row=i, column=1, padx=5, pady=5)

        # Botones
        btn_frame = tk.Frame(master, bg="#F1BB81")
        btn_frame.pack(pady=10)

        self.btn_guardar = tk.Button(btn_frame, text="Guardar Cambios", command=self.guardar_cambios, bg="#E24013")
        self.btn_guardar.grid(row=0, column=0, padx=10)
        self.btn_guardar.config(state="disabled", disabledforeground="black")

        tk.Button(btn_frame, text="Eliminar Animal", command=self.eliminar_animal, bg="#E24013").grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Limpiar Formulario", command=self.limpiar_formulario, bg="#E24013").grid(row=0, column=2, padx=10)

        self.cargar_animales()

    def cargar_animales(self, lista=None):
        recargar_animales()  # Recarga siempre antes de cargar la tabla
        for i in self.tree.get_children():
            self.tree.delete(i)
        datos = lista if lista else animales
        for i, animal in enumerate(datos):
            self.tree.insert("", "end", iid=i, values=(
                animal.get("nombre"),
                animal.get("especie"),
                animal.get("raza"),
                animal.get("edad"),
                animal.get("salud"),
                animal.get("estado_actual")
            ))

    def seleccionar_animal(self, event):
        seleccionado = self.tree.focus()
        if seleccionado:
            self.seleccionado = int(seleccionado)
            animal = animales[self.seleccionado]
            for clave in self.campos:
                self.campos[clave].delete(0, tk.END)
                self.campos[clave].insert(0, animal.get(clave, ""))
            self.btn_guardar.config(state="normal")

    def guardar_cambios(self):
        if self.seleccionado is None:
            return

        datos_editados = {}
        for clave, widget in self.campos.items():
            valor = widget.get().strip()
            if not valor:
                messagebox.showerror("Error", f"El campo '{clave}' no puede estar vacío.")
                return
            if clave == "edad" and not valor.isdigit():
                messagebox.showerror("Error", "La edad debe ser un número.")
                return
            datos_editados[clave] = valor

        animales[self.seleccionado].update(datos_editados)
        guardar_datos(RUTA_ANIMALES, animales)
        self.cargar_animales()
        self.btn_guardar.config(state="disabled")
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        self.limpiar_formulario()

    def eliminar_animal(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un animal para eliminar.")
            return
        idx = int(seleccionado)
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este animal?")
        if confirmacion:
            animales.pop(idx)
            guardar_datos(RUTA_ANIMALES, animales)
            self.cargar_animales()
            self.btn_guardar.config(state="disabled")
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Animal eliminado correctamente.")

    def limpiar_formulario(self):
        for widget in self.campos.values():
            widget.delete(0, tk.END)
        self.btn_guardar.config(state="disabled")
        self.tree.selection_remove(self.tree.focus())

    def aplicar_filtros(self):
        recargar_animales()  # Recargar datos antes de filtrar

        nombre = self.filtro_nombre.get().strip().lower()
        especie = self.filtro_especie.get()
        estado = self.filtro_estado.get()

        filtrados = []
        for animal in animales:
            if nombre and nombre not in animal.get("nombre", "").lower():
                continue
            if especie and especie != animal.get("especie", ""):
                continue
            if estado and estado != animal.get("estado_actual", ""):
                continue
            filtrados.append(animal)

        self.cargar_animales(filtrados)

    def limpiar_filtros(self):
        self.filtro_nombre.delete(0, tk.END)
        self.filtro_especie.set("")
        self.filtro_estado.set("")
        self.cargar_animales()
