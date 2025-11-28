import tkinter as tk
from tkinter import messagebox
from registro_animal import RegistroAnimal
from lista_adopcion import ListaAdopcion
from registrar_adopcion import RegistrarAdopcion
from lista_adoptados import ListaAdoptados
from lista_recuperacion import ListaRecuperacion
from buscar_animal import BuscarAnimal
from reportes import Reportes
from editar_animales import EditarEliminarAnimales
from tkinter import PhotoImage

# Definimos la paleta de colores
PALETA_COLORES = {
    "fondo_principal": "#FB9F85",
    "fondo_menu": "#7F0A31",
    "fondo_contenido": "#F1BB81",
    "boton_bg": "#C56A51",
    "boton_texto": "#000000",
    "texto_general": "#000000"
}

class InterfazInicio:
    def __init__(self, root, rol="empleado"):
        self.root = root
        self.rol = rol
        self.root.title("Refugio de Animales 🐶🐱")
        self.root.geometry("1200x700")
        self.root.configure(bg=PALETA_COLORES["fondo_principal"])

        # Icono personalizado
        try:
            self.root.iconbitmap("assets/huella.ico")
        except FileNotFoundError:
            print("⚠ Icono no encontrado, continuando sin él...")

        # Menú lateral
        self.menu_frame = tk.Frame(self.root, bg=PALETA_COLORES["fondo_menu"], width=220)
        self.menu_frame.pack(side="left", fill="y")

        # Área principal
        self.main_frame = tk.Frame(self.root, bg=PALETA_COLORES["fondo_contenido"])
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Crear menú lateral
        self.crear_menu()

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        self.limpiar_main_frame()

        # Título principal
        tk.Label(self.main_frame, text="SISTEMA DE GESTION " \
        "DE REFUGIO DE ANIMALES", 
                font=("Nunito", 30, "bold"), bg=PALETA_COLORES["fondo_contenido"],
                fg=PALETA_COLORES["texto_general"]).pack(pady=(60, 10))

        # Subtítulo
        tk.Label(self.main_frame, text="¡Bienvenido!", 
                font=("Nunito", 22), bg=PALETA_COLORES["fondo_contenido"],
                fg=PALETA_COLORES["texto_general"]).pack(pady=(0, 30))

        # Imagen centrada
        try:
            self.imagen_inicio = PhotoImage(file="assets/fondo.png")
            tk.Label(self.main_frame, image=self.imagen_inicio, bg=PALETA_COLORES["fondo_contenido"]).pack(pady=20)
        except Exception as e:
            print("⚠ No se pudo cargar la imagen de inicio:", e)


    def crear_menu(self):
        opciones = [
            ("Registrar Nuevo Animal", self.mostrar_registro_animal),
            ("Animales en Adopción", self.mostrar_lista_adopcion),
            ("Registrar Adopción", self.mostrar_registro_adopcion),
            ("Animales Adoptados", self.mostrar_lista_adoptados),
            ("En Recuperación", self.mostrar_lista_recuperacion),
            ("Buscar Animal", self.mostrar_buscar_animal),
            ("Reportes", self.mostrar_reportes),
            ("Editar / Eliminar Animales", self.mostrar_editar_animales)
        ]

        # Si es administrador, agregar opción de usuario
        if self.rol == "administrador":
            opciones.append(("Agregar Usuario", self.mostrar_agregar_usuario))

        opciones.append(("Salir", self.root.quit))

        for texto, comando in opciones:
            tk.Button(self.menu_frame, text=texto, command=comando,
                      font=("Arial", 10), bg=PALETA_COLORES["boton_bg"], fg=PALETA_COLORES["boton_texto"],
                      bd=0, padx=10, pady=10).pack(pady=5, padx=10, fill="x")

    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_registro_animal(self):
        self.limpiar_main_frame()
        RegistroAnimal(self.main_frame)

    def mostrar_lista_adopcion(self):
        self.limpiar_main_frame()
        ListaAdopcion(self.main_frame)

    def mostrar_registro_adopcion(self):
        self.limpiar_main_frame()
        RegistrarAdopcion(self.main_frame)

    def mostrar_lista_adoptados(self):
        self.limpiar_main_frame()
        ListaAdoptados(self.main_frame)

    def mostrar_lista_recuperacion(self):
        self.limpiar_main_frame()
        ListaRecuperacion(self.main_frame)

    def mostrar_buscar_animal(self):
        self.limpiar_main_frame()
        BuscarAnimal(self.main_frame)

    def mostrar_reportes(self):
        self.limpiar_main_frame()
        Reportes(self.main_frame)

    def mostrar_editar_animales(self):
        self.limpiar_main_frame()
        EditarEliminarAnimales(self.main_frame)

    def mostrar_agregar_usuario(self):
        from agregar_usuario import AgregarUsuario
        self.limpiar_main_frame()
        AgregarUsuario(self.main_frame)