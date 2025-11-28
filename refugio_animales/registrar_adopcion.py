import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datos.datos_animales import animales, guardar_datos, RUTA_ANIMALES
from datos.datos_animales import animales, guardar_datos, RUTA_ANIMALES, adopciones, RUTA_ADOPCIONES
import re

class RegistrarAdopcion:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="#F1BB81")
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="Registrar Adopción 🏠",
            font=("Arial", 18), bg="#F1BB81"
        ).pack(pady=20)

        form_frame = tk.Frame(self.frame, bg="#F1BB81")
        form_frame.pack(pady=10)

        # Lista de animales en adopción
        tk.Label(form_frame, text="Animal:", font=("Arial", 12), bg="#F1BB81")\
            .grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.combo_animales = ttk.Combobox(
            form_frame, values=[a["nombre"] for a in animales if a.get("estado_actual") == "En Adopción"], state="readonly"
        )
        self.combo_animales.grid(row=0, column=1, pady=5, padx=5)

        campos = [
            ("Nombre del Adoptante", "nombre"),
            ("Correo Electrónico", "correo"),
            ("Teléfono", "telefono"),
            ("Notas (opcional)", "notas")
        ]

        self.entradas = {}

        for i, (etiqueta, clave) in enumerate(campos, start=1):
            tk.Label(form_frame, text=etiqueta, font=("Arial", 12), bg="#F1BB81")\
                .grid(row=i, column=0, sticky="e", pady=5, padx=5)

            entrada = tk.Entry(form_frame, width=40)
            entrada.grid(row=i, column=1, pady=5, padx=5)
            self.entradas[clave] = entrada

        # Subir INE
        self.ine_path = tk.StringVar()
        tk.Button(form_frame, text="Subir Foto de INE", command=self.subir_ine).grid(row=len(campos)+1, column=0, pady=10)
        tk.Label(form_frame, textvariable=self.ine_path, bg="#F1BB81").grid(row=len(campos)+1, column=1, pady=10)

        # Botón guardar
        tk.Button(
            self.frame, text="Registrar Adopción", bg="#C72213", fg="white", font=("Arial", 14),
            command=self.validar_datos
        ).pack(pady=20)

    def subir_ine(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            self.ine_path.set(ruta)

    def validar_datos(self):
        animal_nombre = self.combo_animales.get().strip()
        datos = {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}
        datos["ine"] = self.ine_path.get().strip()

        if not animal_nombre or not datos["nombre"] or not datos["correo"] or not datos["telefono"]:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", datos["correo"]):
            messagebox.showerror("Error", "Correo electrónico inválido.")
            return

        if not datos["telefono"].isdigit() or len(datos["telefono"]) != 10:
            messagebox.showerror("Error", "El número de teléfono debe tener 10 dígitos.")
            return

        for animal in animales:
            if animal["nombre"] == animal_nombre and animal.get("estado_actual") == "En Adopción":
                animal["estado_actual"] = "Adoptado"
                animal["adoptante"] = datos

                # Crear entrada de adopción
                from datetime import datetime
                adopcion = {
                    "animal": animal["nombre"],
                    "especie": animal["especie"],
                    "edad": animal["edad"],
                    "salud": animal["salud"],
                    "adoptante": datos["nombre"],
                    "correo": datos["correo"],
                    "telefono": datos["telefono"],
                    "ine": datos["ine"],
                    "notas": datos.get("notas", ""),
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                adopciones.append(adopcion)
                guardar_datos(RUTA_ADOPCIONES, adopciones)

                break
        else:
            messagebox.showerror("Error", "El animal seleccionado no está disponible para adopción.")
            return

        guardar_datos(RUTA_ANIMALES, animales)
        messagebox.showinfo("Éxito", "Adopción registrada correctamente 🐾")
        self.limpiar_formulario()


    def limpiar_formulario(self):
        self.combo_animales.set("")
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.ine_path.set("")
