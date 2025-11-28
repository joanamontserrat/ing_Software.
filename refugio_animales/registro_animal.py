import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datos.datos_animales import animales, guardar_datos, RUTA_ANIMALES

class RegistroAnimal:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#F1BB81")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="Registrar Nuevo Animal 🐾",
            font=("Arial", 18), bg="#F1BB81"
        ).pack(pady=20)

        # ----- Formulario -----
        form_frame = tk.Frame(self.frame, bg="#F1BB81")
        form_frame.pack(pady=10)

        campos = [
            ("Nombre", "nombre"),
            ("Especie", "especie"),
            ("Raza", "raza"),
            ("Edad", "edad"),
            ("Estado de Salud", "salud"),
            ("Estado Inicial", "estado")
        ]

        self.entradas = {}

        for i, (etiqueta, clave) in enumerate(campos):
            tk.Label(form_frame, text=etiqueta, font=("Arial", 12), bg="#F1BB81")\
                .grid(row=i, column=0, sticky="e", pady=5, padx=5)

            if clave == "especie":
                entrada = ttk.Combobox(form_frame, values=["Perro", "Gato", "Otro"], state="readonly")
            elif clave == "salud":
                entrada = ttk.Combobox(form_frame, values=["Buena", "Regular", "Grave"], state="readonly")
            elif clave == "estado":
                entrada = ttk.Combobox(form_frame, values=["Rescatado", "Reportado"], state="readonly")
            else:
                entrada = tk.Entry(form_frame)

            entrada.grid(row=i, column=1, pady=5, padx=5)
            self.entradas[clave] = entrada

        # Campo para foto
        self.foto_path = tk.StringVar()
        tk.Button(form_frame, text="Subir Foto", command=self.subir_foto).grid(row=len(campos), column=0, pady=10)
        tk.Label(form_frame, textvariable=self.foto_path, bg="#F1BB81").grid(row=len(campos), column=1, pady=10)

        # Botón guardar con validación
        tk.Button(
            self.frame, text="Guardar Registro", bg="#C72213", fg="white", font=("Arial", 14),
            command=self.validar_datos
        ).pack(pady=20)

    def subir_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            self.foto_path.set(ruta)

    def validar_datos(self):
        datos = {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}
        datos["foto"] = self.foto_path.get().strip()
        datos["estado_actual"] = "En Adopción"

        # Validar campos vacíos
        if not all(datos.values()):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        # Validar que la edad sea un número entero positivo
        if not datos["edad"].isdigit() or int(datos["edad"]) <= 0:
            messagebox.showerror("Error", "La edad debe ser un número entero positivo.")
            return

        # Si todo es válido, guardar
        self.guardar_animal(datos)

    def guardar_animal(self, datos):
        animales.append(datos)
        guardar_datos(RUTA_ANIMALES, animales)
        messagebox.showinfo("Éxito", "Animal registrado correctamente 🐶")
        self.limpiar_formulario()

    def limpiar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.foto_path.set("")
