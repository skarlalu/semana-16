import json
import os
from pathlib import Path


class ArchivoServicio:
    BASE_DIR = Path(__file__).resolve().parent.parent
    RUTA_PRODUCTOS = str(BASE_DIR / "datos" / "productos.json")
    RUTA_USUARIOS = str(BASE_DIR / "datos" / "usuarios.json")
    RUTA_VENTAS = str(BASE_DIR / "datos" / "ventas.json")

    @staticmethod
    def cargar_json(ruta: str) -> list:
        try:
            if not os.path.exists(ruta):
                return []
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos if isinstance(datos, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def guardar_json(ruta: str, datos: list):
        directorio = os.path.dirname(ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
