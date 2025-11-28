import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib

class AgregarUsuario:
    RUTA_USUARIOS = "datos/datosusuarios.json"
    ROLES = ["empleado", "administrador"]
    ROL_POR_DEFECTO = "empleado"

    def __init__(self, frame):
        self.frame = frame
        self.frame.configure(bg="#F1BB81")

        tk.Label(frame, text="Agregar Nuevo Usuario", font=("Arial", 16, "bold"), bg="#F1BB81").pack(pady=20)

        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.rol_var = tk.StringVar(value=self.ROL_POR_DEFECTO)

        form_frame = tk.Frame(frame, bg="#F1BB81")
        form_frame.pack(pady=10)

        # Usuario
        tk.Label(form_frame, text="Usuario:", bg="#F1BB81").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(form_frame, textvariable=self.usuario_var, width=30).grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        tk.Label(form_frame, text="Contraseña:", bg="#F1BB81").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.contrasena_entry = tk.Entry(form_frame, textvariable=self.contrasena_var, show="*", width=30)
        self.contrasena_entry.grid(row=1, column=1, padx=10, pady=5)

        self.mostrar_var = tk.IntVar()
        tk.Checkbutton(form_frame, text="Mostrar contraseña", variable=self.mostrar_var,
                       command=self.toggle_password, bg="#F1BB81").grid(row=1, column=2, padx=5)

        # Rol
        tk.Label(form_frame, text="Rol:", bg="#F1BB81").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.OptionMenu(form_frame, self.rol_var, *self.ROLES).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Botón para guardar
        tk.Button(frame, text="Agregar Usuario", command=self.guardar_usuario,
                  bg="#C72213", fg="white", font=("Arial", 10), padx=10, pady=5).pack(pady=20)

    def toggle_password(self):
        self.contrasena_entry.config(show="" if self.mostrar_var.get() else "*")

    def guardar_usuario(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()
        rol = self.rol_var.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return

        if len(contrasena) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return

        if not os.path.exists("datos"):
            os.makedirs("datos")

        usuarios = self.cargar_usuarios()

        if any(u["usuario"] == usuario for u in usuarios):
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return

        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

        usuarios.append({
            "usuario": usuario,
            "contrasena": hash_contrasena,
            "rol": rol
        })

        self.guardar_usuarios(usuarios)

        messagebox.showinfo("Éxito", f"Usuario '{usuario}' agregado exitosamente.")
        self.limpiar_campos()

    def cargar_usuarios(self):
        if os.path.exists(self.RUTA_USUARIOS):
            try:
                with open(self.RUTA_USUARIOS, "r") as archivo:
                    return json.load(archivo)
            except json.JSONDecodeError:
                return []
        return []

    def guardar_usuarios(self, usuarios):
        with open(self.RUTA_USUARIOS, "w") as archivo:
            json.dump(usuarios, archivo, indent=4)

    def limpiar_campos(self):
        self.usuario_var.set("")
        self.contrasena_var.set("")
        self.rol_var.set(self.ROL_POR_DEFECTO)
        self.mostrar_var.set(0)
        self.toggle_password()
