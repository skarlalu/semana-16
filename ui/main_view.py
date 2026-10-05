import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


class MainView(tk.Frame):
    def __init__(self, parent, controlador, servicio, usuario_actual):
        super().__init__(parent, bg="#f5f6fa")
        self.controlador = controlador
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.iconos = {}
        self.usuario_seleccionado_id = None

        self._cargar_iconos()

        top_frame = tk.Frame(self, bg="#2c3e50", height=70)
        top_frame.pack(side="top", fill="x")

        logo_frame = tk.Frame(top_frame, bg="#2c3e50")
        logo_frame.pack(side="left", padx=12, pady=7)
        self.logo_header = None
        self._cargar_logo_header(logo_frame)

        tk.Label(
            top_frame,
            text="Sistema de Gestión - Restaurante App",
            fg="white",
            bg="#2c3e50",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=8, pady=10)

        info_usuario = f"{self.usuario_actual.nombre} | {self.usuario_actual.rol}"
        tk.Label(
            top_frame,
            text=info_usuario,
            fg="white",
            bg="#2c3e50",
            font=("Arial", 9)
        ).pack(side="right", padx=(5, 12), pady=10)

        tk.Button(
            top_frame,
            text="Cerrar Sesión",
            bg="#e74c3c",
            fg="white",
            command=self.controlador.cerrar_sesion
        ).pack(side="right", padx=5, pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_productos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_productos, text="Productos")
        self.crear_seccion_productos()

        if self.usuario_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_usuarios, text="Usuarios")
            self.crear_seccion_usuarios()

        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.crear_seccion_ventas()

    def _cargar_logo_header(self, contenedor):
        ruta = str(Path(__file__).resolve().parent.parent / "assets" / "logo.png")
        if not os.path.exists(ruta):
            return
        try:
            self.logo_header = tk.PhotoImage(file=ruta)
            factor = max(1, self.logo_header.width() // 115)
            if factor > 1:
                self.logo_header = self.logo_header.subsample(factor, factor)
            tk.Label(contenedor, image=self.logo_header, bg="#2c3e50").pack()
        except tk.TclError:
            pass

    def _cargar_iconos(self):
        for nombre in ("productos", "usuarios", "ventas"):
            ruta = str(Path(__file__).resolve().parent.parent / "assets" / f"icono_{nombre}.png")
            if os.path.exists(ruta):
                try:
                    self.iconos[nombre] = tk.PhotoImage(file=ruta)
                except tk.TclError:
                    pass

    # ========================= PRODUCTOS =========================
    def crear_seccion_productos(self):
        frame_form = tk.LabelFrame(
            self.tab_productos,
            text=" Formulario de Producto ",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        campos = [
            ("Código:", "txt_codigo"),
            ("Nombre:", "txt_nombre"),
            ("Categoría:", "txt_categoria"),
            ("Precio:", "txt_precio"),
            ("Stock:", "txt_stock")
        ]
        for fila, (texto, atributo) in enumerate(campos):
            tk.Label(frame_form, text=texto).grid(row=fila, column=0, sticky="w", pady=5)
            entrada = tk.Entry(frame_form, width=20)
            entrada.grid(row=fila, column=1, pady=5)
            setattr(self, atributo, entrada)

        frame_botones = tk.Frame(frame_form)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(frame_botones, text="Registrar", bg="#2ecc71", fg="white", width=10, command=self.registrar).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Consultar", bg="#3498db", fg="white", width=10, command=self.consultar).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_botones, text="Actualizar", bg="#f39c12", fg="white", width=10, command=self.actualizar).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Eliminar", bg="#e74c3c", fg="white", width=10, command=self.eliminar).grid(row=1, column=1, padx=5, pady=5)

        frame_tabla = tk.LabelFrame(
            self.tab_productos,
            text=" Listado de Productos Registrados ",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columns = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        for col in columns:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=90)
        self.tabla.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for p in self.servicio.productos:
            self.tabla.insert("", "end", values=(p.codigo, p.nombre, p.categoria, f"${p.precio:.2f}", p.stock))

    def registrar(self):
        try:
            self.servicio.registrar_producto(
                self.txt_codigo.get(), self.txt_nombre.get(), self.txt_categoria.get(),
                self.txt_precio.get(), self.txt_stock.get()
            )
            self.actualizar_tabla()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def consultar(self):
        p = self.servicio.buscar_producto(self.txt_codigo.get())
        if p:
            for entrada, valor in (
                (self.txt_nombre, p.nombre),
                (self.txt_categoria, p.categoria),
                (self.txt_precio, str(p.precio)),
                (self.txt_stock, str(p.stock))
            ):
                entrada.delete(0, tk.END)
                entrada.insert(0, valor)
        else:
            messagebox.showwarning("No encontrado", "No existe un producto con ese código.")

    def actualizar(self):
        try:
            self.servicio.actualizar_producto(
                self.txt_codigo.get(), self.txt_nombre.get(), self.txt_categoria.get(),
                self.txt_precio.get(), self.txt_stock.get()
            )
            self.actualizar_tabla()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        try:
            self.servicio.eliminar_producto(self.txt_codigo.get())
            self.actualizar_tabla()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        for entrada in (self.txt_codigo, self.txt_nombre, self.txt_categoria, self.txt_precio, self.txt_stock):
            entrada.delete(0, tk.END)

    # ========================= USUARIOS - SEMANA 16 =========================
    def crear_seccion_usuarios(self):
        contenedor = tk.Frame(self.tab_usuarios, padx=15, pady=12, bg="#f5f6fa")
        contenedor.pack(fill="both", expand=True)

        encabezado = tk.Frame(contenedor, bg="#f5f6fa")
        encabezado.pack(fill="x", pady=(0, 8))
        if "usuarios" in self.iconos:
            tk.Label(encabezado, image=self.iconos["usuarios"], bg="#f5f6fa").pack(side="left", padx=(0, 8))
        tk.Label(
            encabezado,
            text="Gestión de Usuarios",
            font=("Arial", 14, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(side="left")
        tk.Label(
            encabezado,
            text="Solo disponible para Administrador",
            font=("Arial", 9),
            bg="#f5f6fa",
            fg="#7f8c8d"
        ).pack(side="right")

        panel = tk.Frame(contenedor, bg="#f5f6fa")
        panel.pack(fill="both", expand=True)

        frame_form = tk.LabelFrame(
            panel,
            text=" Datos del usuario ",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=10
        )
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(frame_form, text="Identificación:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_usuario_id = tk.Entry(frame_form, width=25)
        self.txt_usuario_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_usuario_nombre = tk.Entry(frame_form, width=25)
        self.txt_usuario_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo / Usuario:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.txt_usuario_correo = tk.Entry(frame_form, width=25)
        self.txt_usuario_correo.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Contraseña:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.txt_usuario_clave = tk.Entry(frame_form, show="*", width=25)
        self.txt_usuario_clave.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Rol:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.combo_rol = ttk.Combobox(
            frame_form,
            values=("Administrador", "Empleado", "Cliente"),
            state="readonly",
            width=22
        )
        self.combo_rol.grid(row=4, column=1, padx=5, pady=5)
        self.combo_rol.set("Cliente")
        self.combo_rol.bind("<<ComboboxSelected>>", self.evento_rol_seleccionado)

        self.lbl_evento_rol = tk.Label(
            frame_form,
            text="Rol seleccionado: Cliente",
            fg="#7f8c8d",
            font=("Arial", 9),
            anchor="w"
        )
        self.lbl_evento_rol.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=(2, 8))

        frame_botones = tk.Frame(frame_form)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=8)

        tk.Button(
            frame_botones, text="Registrar", bg="#2ecc71", fg="white", width=11,
            command=self.registrar_usuario
        ).grid(row=0, column=0, padx=3, pady=4)
        tk.Button(
            frame_botones, text="Actualizar", bg="#f39c12", fg="white", width=11,
            command=self.actualizar_usuario
        ).grid(row=0, column=1, padx=3, pady=4)
        tk.Button(
            frame_botones, text="Eliminar", bg="#e74c3c", fg="white", width=11,
            command=self.eliminar_usuario
        ).grid(row=1, column=0, padx=3, pady=4)
        tk.Button(
            frame_botones, text="Limpiar", bg="#7f8c8d", fg="white", width=11,
            command=self.limpiar_usuario
        ).grid(row=1, column=1, padx=3, pady=4)

        tk.Label(
            frame_form,
            text="Enter: registrar | Escape: limpiar",
            font=("Arial", 8),
            fg="#7f8c8d"
        ).grid(row=7, column=0, columnspan=2, pady=(5, 0))

        frame_tabla = tk.LabelFrame(
            panel,
            text=" Usuarios registrados ",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8
        )
        frame_tabla.pack(side="right", fill="both", expand=True)

        columns = ("id", "nombre", "correo", "rol")
        self.tabla_usuarios = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=12)
        encabezados = {
            "id": "Identificación",
            "nombre": "Nombre",
            "correo": "Usuario / Correo",
            "rol": "Rol"
        }
        anchos = {"id": 100, "nombre": 150, "correo": 180, "rol": 105}
        for col in columns:
            self.tabla_usuarios.heading(col, text=encabezados[col])
            self.tabla_usuarios.column(col, width=anchos[col], anchor="w")
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)

        # Eventos solicitados en la Semana 16.
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.evento_usuario_seleccionado)
        self.tabla_usuarios.bind("<Escape>", self.evento_escape)

        # <Return> se reutiliza como atajo para el registro y <Escape> para limpiar.
        for widget in (
            self.txt_usuario_id,
            self.txt_usuario_nombre,
            self.txt_usuario_correo,
            self.txt_usuario_clave,
            self.combo_rol
        ):
            widget.bind("<Return>", self.evento_return)
            widget.bind("<Escape>", self.evento_escape)

        self.actualizar_tabla_usuarios()

    def actualizar_tabla_usuarios(self):
        for row in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(row)

        for u in self.servicio.usuarios:
            # La contraseña no se muestra por seguridad.
            self.tabla_usuarios.insert(
                "", "end",
                values=(u.identificacion, u.nombre, u.correo, u.rol)
            )

    def evento_usuario_seleccionado(self, event):
        """Callback de <<TreeviewSelect>>: obtiene el ID y consulta el objeto en el servicio."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        identificacion = valores[0]
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showwarning("Usuario no encontrado", "No se encontró el usuario seleccionado.")
            return

        self.usuario_seleccionado_id = usuario.identificacion
        self._cargar_usuario_en_formulario(usuario)

    def _cargar_usuario_en_formulario(self, usuario):
        self._establecer_entry(self.txt_usuario_id, usuario.identificacion)
        self._establecer_entry(self.txt_usuario_nombre, usuario.nombre)
        self._establecer_entry(self.txt_usuario_correo, usuario.correo)
        self._establecer_entry(self.txt_usuario_clave, usuario.clave)
        self.combo_rol.set(usuario.rol)
        self.lbl_evento_rol.config(text=f"Rol seleccionado: {usuario.rol}")
        self.txt_usuario_id.config(state="disabled")

    @staticmethod
    def _establecer_entry(entry, valor):
        estado = str(entry.cget("state"))
        if estado == "disabled":
            entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, valor)

    def evento_return(self, event):
        """Callback de <Return>. Reutiliza la lógica existente de registrar_usuario()."""
        self.registrar_usuario()
        return "break"

    def evento_escape(self, event=None):
        """Callback de <Escape>. Limpia formulario y selección actual."""
        self.limpiar_usuario()
        return "break"

    def evento_rol_seleccionado(self, event):
        """Callback de <<ComboboxSelected>> para responder al cambio de rol."""
        rol = self.combo_rol.get()
        self.lbl_evento_rol.config(text=f"Rol seleccionado: {rol}")

    def registrar_usuario(self):
        try:
            nuevo = self.servicio.registrar_usuario(
                self.txt_usuario_id.get(),
                self.txt_usuario_nombre.get(),
                self.txt_usuario_correo.get(),
                self.txt_usuario_clave.get(),
                self.combo_rol.get()
            )
            self.actualizar_tabla_usuarios()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", f"El usuario {nuevo.nombre} fue registrado correctamente.")
            self.limpiar_usuario()
        except Exception as e:
            messagebox.showerror("Error al registrar usuario", str(e))

    def actualizar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Selección requerida", "Seleccione un usuario en el Treeview antes de actualizar.")
            return

        try:
            usuario = self.servicio.actualizar_usuario(
                self.usuario_seleccionado_id,
                self.txt_usuario_nombre.get(),
                self.txt_usuario_correo.get(),
                self.txt_usuario_clave.get(),
                self.combo_rol.get(),
                self.usuario_actual.identificacion
            )
            self.actualizar_tabla_usuarios()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", f"El usuario {usuario.nombre} fue actualizado correctamente.")
            self.limpiar_usuario()
        except Exception as e:
            messagebox.showerror("Error al actualizar usuario", str(e))

    def eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Selección requerida", "Seleccione un usuario en el Treeview antes de eliminar.")
            return

        if self.usuario_seleccionado_id == self.usuario_actual.identificacion:
            messagebox.showwarning(
                "Operación no permitida",
                "No puede eliminar la cuenta administrativa actualmente autenticada."
            )
            return

        usuario = self.servicio.buscar_usuario(self.usuario_seleccionado_id)
        if usuario is None:
            messagebox.showwarning("Usuario no encontrado", "El usuario seleccionado ya no existe.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar al usuario {usuario.nombre}?"
        )
        if not confirmar:
            return

        try:
            self.servicio.eliminar_usuario(
                self.usuario_seleccionado_id,
                self.usuario_actual.identificacion
            )
            self.actualizar_tabla_usuarios()
            self.actualizar_combos_ventas()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self.limpiar_usuario()
        except Exception as e:
            messagebox.showerror("Error al eliminar usuario", str(e))

    def limpiar_usuario(self):
        self._establecer_entry(self.txt_usuario_id, "")
        self._establecer_entry(self.txt_usuario_nombre, "")
        self._establecer_entry(self.txt_usuario_correo, "")
        self._establecer_entry(self.txt_usuario_clave, "")
        self.txt_usuario_id.config(state="normal")
        self.combo_rol.set("Cliente")
        self.lbl_evento_rol.config(text="Rol seleccionado: Cliente")
        self.usuario_seleccionado_id = None
        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)

    # ========================= VENTAS =========================
    def crear_seccion_ventas(self):
        contenedor = tk.Frame(self.tab_ventas, padx=15, pady=15, bg="#f5f6fa")
        contenedor.pack(fill="both", expand=True)

        encabezado = tk.Frame(contenedor, bg="#f5f6fa")
        encabezado.pack(fill="x", pady=(0, 10))
        if "ventas" in self.iconos:
            tk.Label(encabezado, image=self.iconos["ventas"], bg="#f5f6fa").pack(side="left", padx=(0, 8))
        tk.Label(encabezado, text="Registro de Ventas", font=("Arial", 14, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(side="left")

        frame_form = tk.LabelFrame(
            contenedor,
            text=" Nueva Venta ",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        frame_form.pack(fill="x", pady=(0, 10))

        tk.Label(frame_form, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_usuario = ttk.Combobox(frame_form, state="readonly", width=35)
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_form, state="readonly", width=35)
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            frame_form,
            text="Registrar venta",
            bg="#e67e22",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            command=self.registrar_venta
        ).grid(row=0, column=2, rowspan=2, padx=20, pady=5)

        frame_tabla = tk.LabelFrame(
            contenedor,
            text=" Ventas Registradas ",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        frame_tabla.pack(fill="both", expand=True)

        columns = ("usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=9)
        self.tabla_ventas.heading("usuario", text="Usuario")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.column("usuario", width=180)
        self.tabla_ventas.column("producto", width=230)
        self.tabla_ventas.column("fecha", width=180)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_ventas.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)

        self.actualizar_combos_ventas()
        self.actualizar_tabla_ventas()

    def actualizar_combos_ventas(self):
        if not hasattr(self, "combo_usuario"):
            return

        usuarios = [f"{u.identificacion} - {u.nombre}" for u in self.servicio.usuarios]
        productos = [f"{p.codigo} - {p.nombre}" for p in self.servicio.productos]
        self.combo_usuario["values"] = usuarios
        self.combo_producto["values"] = productos

        if usuarios and self.combo_usuario.get() not in usuarios:
            self.combo_usuario.current(0)
        elif not usuarios:
            self.combo_usuario.set("")

        if productos and self.combo_producto.get() not in productos:
            self.combo_producto.current(0)
        elif not productos:
            self.combo_producto.set("")

    def registrar_venta(self):
        usuario_seleccionado = self.combo_usuario.get()
        producto_seleccionado = self.combo_producto.get()

        if not usuario_seleccionado or not producto_seleccionado:
            messagebox.showwarning("Datos incompletos", "Seleccione un usuario y un producto.")
            return

        usuario_id = usuario_seleccionado.split(" - ", 1)[0]
        producto_codigo = producto_seleccionado.split(" - ", 1)[0]

        try:
            self.servicio.registrar_venta(usuario_id, producto_codigo)
            self.actualizar_tabla_ventas()
            messagebox.showinfo("Venta registrada", "La venta se registró correctamente y se guardó en ventas.json.")
        except Exception as e:
            messagebox.showerror("Error al registrar venta", str(e))

    def actualizar_tabla_ventas(self):
        if not hasattr(self, "tabla_ventas"):
            return

        for row in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(row)

        for venta in self.servicio.ventas:
            usuario = self.servicio.buscar_usuario(venta.usuario_id)
            producto = self.servicio.buscar_producto(venta.producto_codigo)
            nombre_usuario = usuario.nombre if usuario else venta.usuario_id
            nombre_producto = producto.nombre if producto else venta.producto_codigo
            self.tabla_ventas.insert("", "end", values=(nombre_usuario, nombre_producto, venta.fecha))
