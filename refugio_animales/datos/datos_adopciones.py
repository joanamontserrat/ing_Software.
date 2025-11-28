import json
import os

RUTA_ADOPCIONES = os.path.join('datos', 'adopciones.json')

def cargar_datos(ruta=RUTA_ADOPCIONES):
    try:
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error cargando adopciones: {e}")
        return []

def guardar_datos(ruta, datos):
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando adopciones: {e}")
        