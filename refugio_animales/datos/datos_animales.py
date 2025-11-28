import json
import os

# Rutas de los archivos
RUTA_ANIMALES = "datos/animales.json"
RUTA_ADOPCIONES = "datos/adopciones.json"

# Cargar datos al iniciar
def cargar_datos(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar datos al cerrar
def guardar_datos(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Recargar animales (actualiza la variable global animales)
def recargar_animales():
    global animales
    animales = cargar_datos(RUTA_ANIMALES)

# Datos compartidos por todo el sistema
animales = cargar_datos(RUTA_ANIMALES)
adopciones = cargar_datos(RUTA_ADOPCIONES)
