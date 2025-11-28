import json
import os

RUTA_USUARIOS = "datos/datosusuarios.json"  # <--- esta línea es clave

def verificar_credenciales(usuario, contrasena):
    if not os.path.exists(RUTA_USUARIOS):
        return None

    with open(RUTA_USUARIOS, "r") as archivo:
        try:
            usuarios = json.load(archivo)
        except json.JSONDecodeError:
            return None

    for u in usuarios:
        if u["usuario"] == usuario and u["contrasena"] == contrasena:
            return u["rol"]

    return None
