import tkinter as tk
from tkinter import messagebox
from interfaz_inicio import InterfazInicio
from datos.datos_usuarios import verificar_credenciales

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Iniciar Sesión")
        self.root.geometry("350x250")
        self.root.configure(bg="#FF7F51")

        tk.Label(root, text="Usuario:", font=("Arial", 12), bg="#FF7F51").pack(pady=10)
        self.usuario_entry = tk.Entry(root, font=("Arial", 12))
        self.usuario_entry.pack()

        tk.Label(root, text="Contraseña:", font=("Arial", 12), bg="#FF7F51").pack(pady=10)
        self.contrasena_entry = tk.Entry(root, show="*", font=("Arial", 12))
        self.contrasena_entry.pack()

        self.ver_var = tk.IntVar()
        tk.Checkbutton(root, text="Mostrar contraseña", variable=self.ver_var,
                       command=self.toggle_password, bg="#B93513",fg="white").pack(pady=5)

        tk.Button(root, text="Ingresar", command=self.iniciar_sesion,
                  bg="#720026", fg="white", font=("Arial", 12)).pack(pady=20)

    def toggle_password(self):
        self.contrasena_entry.config(show="" if self.ver_var.get() else "*")

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña.")
            return

        rol = verificar_credenciales(usuario, contrasena)

        if rol:
            for widget in self.root.winfo_children():
                widget.destroy()
            InterfazInicio(self.root, rol=rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
