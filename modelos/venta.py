from datetime import datetime


class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, fecha: str = ""):
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha
        }
