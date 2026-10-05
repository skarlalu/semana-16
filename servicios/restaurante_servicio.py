from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self):
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        u_data = ArchivoServicio.cargar_json(ArchivoServicio.RUTA_USUARIOS)
        self.usuarios = [
            Usuario(u["identificacion"], u["nombre"], u["correo"], u.get("clave", ""), u.get("rol", "Cliente"))
            for u in u_data
        ]

        p_data = ArchivoServicio.cargar_json(ArchivoServicio.RUTA_PRODUCTOS)
        self.productos = [
            Producto(
                p["codigo"],
                p["nombre"],
                p["categoria"],
                float(p["precio"]),
                int(p.get("stock", 0))
            )
            for p in p_data
        ]

        v_data = ArchivoServicio.cargar_json(ArchivoServicio.RUTA_VENTAS)
        self.ventas = [
            Venta(v["usuario_id"], v["producto_codigo"], v.get("fecha", ""))
            for v in v_data
            if "usuario_id" in v and "producto_codigo" in v
        ]

    def guardar_productos(self):
        p_data = [p.a_diccionario() for p in self.productos]
        ArchivoServicio.guardar_json(ArchivoServicio.RUTA_PRODUCTOS, p_data)

    def guardar_ventas(self):
        v_data = [v.a_diccionario() for v in self.ventas]
        ArchivoServicio.guardar_json(ArchivoServicio.RUTA_VENTAS, v_data)

    def autenticar_usuario(self, correo: str, clave: str):
        """Devuelve el usuario autenticado o None si las credenciales no son válidas."""
        for usuario in self.usuarios:
            if usuario.correo == correo and (not usuario.clave or usuario.clave == clave):
                return usuario

        if not self.usuarios and correo == "admin" and clave == "admin":
            return Usuario("1", "Administrador", "admin", "admin", "Administrador")
        return None

    def validar_login(self, correo: str, clave: str) -> bool:
        """Mantiene compatibilidad con la versión anterior del proyecto."""
        return self.autenticar_usuario(correo, clave) is not None

    def guardar_usuarios(self):
        u_data = [u.a_diccionario() for u in self.usuarios]
        ArchivoServicio.guardar_json(ArchivoServicio.RUTA_USUARIOS, u_data)

    def registrar_usuario(self, identificacion: str, nombre: str, correo: str, clave: str, rol: str):
        identificacion = identificacion.strip()
        nombre = nombre.strip()
        correo = correo.strip()
        rol = rol.strip()

        if not identificacion or not nombre or not correo or not clave:
            raise ValueError("Identificación, nombre, correo y contraseña son obligatorios.")
        if rol not in Usuario.ROLES:
            raise ValueError("Seleccione un rol válido.")

        if self.buscar_usuario(identificacion):
            raise ValueError("Ya existe un usuario con esa identificación.")

        if any(u.correo.lower() == correo.lower() for u in self.usuarios):
            raise ValueError("Ya existe un usuario con ese correo.")

        nuevo = Usuario(identificacion, nombre, correo, clave, rol)
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, identificacion_original: str, nombre: str, correo: str, clave: str, rol: str, identificacion_autenticado: str = ""):
        nombre = nombre.strip()
        correo = correo.strip()
        rol = rol.strip()

        if not nombre or not correo or not clave:
            raise ValueError("Nombre, correo y contraseña son obligatorios.")
        if rol not in Usuario.ROLES:
            raise ValueError("Seleccione un rol válido.")
        if identificacion_original == identificacion_autenticado and rol != "Administrador":
            raise ValueError("La cuenta administrativa actualmente autenticada debe conservar el rol Administrador.")

        usuario = self.buscar_usuario(identificacion_original)
        if usuario is None:
            raise ValueError("No se encontró el usuario seleccionado.")

        for otro in self.usuarios:
            if otro is not usuario and otro.correo.lower() == correo.lower():
                raise ValueError("Ya existe otro usuario con ese correo.")

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.clave = clave
        usuario.rol = rol
        self.guardar_usuarios()
        return usuario

    def eliminar_usuario(self, identificacion: str, identificacion_autenticado: str = ""):
        if identificacion == identificacion_autenticado:
            raise ValueError("No puede eliminar la cuenta del administrador que está actualmente autenticado.")

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            raise ValueError("No se encontró el usuario seleccionado.")

        self.usuarios.remove(usuario)
        self.guardar_usuarios()
        return True

    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int):
        if not codigo.strip() or not nombre.strip():
            raise ValueError("El código y el nombre son obligatorios.")

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            raise ValueError("El precio debe ser numérico y el stock debe ser entero.")

        if precio < 0 or stock < 0:
            raise ValueError("El precio y el stock no pueden ser negativos.")

        for p in self.productos:
            if p.codigo == codigo.strip():
                raise ValueError("Ya existe un producto con ese código.")

        nuevo = Producto(codigo.strip(), nombre.strip(), categoria.strip(), precio, stock)
        self.productos.append(nuevo)
        self.guardar_productos()

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int):
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            raise ValueError("El precio debe ser numérico y el stock debe ser entero.")

        for p in self.productos:
            if p.codigo == codigo:
                p.nombre = nombre.strip()
                p.categoria = categoria.strip()
                p.precio = precio
                p.stock = stock
                self.guardar_productos()
                return True
        raise ValueError("No se encontró un producto con el código especificado.")

    def eliminar_producto(self, codigo: str):
        for p in self.productos:
            if p.codigo == codigo:
                self.productos.remove(p)
                self.guardar_productos()
                return True
        raise ValueError("No se encontró el producto a eliminar.")

    def buscar_producto(self, codigo: str):
        for p in self.productos:
            if p.codigo == codigo:
                return p
        return None

    def buscar_usuario(self, identificacion: str):
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def registrar_venta(self, usuario_id: str, producto_codigo: str):
        usuario = self.buscar_usuario(usuario_id)
        if usuario is None:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        if producto.stock <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        venta = Venta(usuario.identificacion, producto.codigo)
        self.ventas.append(venta)
        self.guardar_ventas()
        return venta
