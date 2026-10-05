class Usuario:
    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion: str, nombre: str, correo: str, clave: str = "", rol: str = "Cliente"):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.rol = rol if rol in self.ROLES else "Cliente"

    def a_diccionario(self) -> dict:
        """Convierte el objeto Usuario en un diccionario para persistencia."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "clave": self.clave,
            "rol": self.rol
        }
