import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


class LoginView(tk.Frame):
    def __init__(self, parent, controlador, servicio):
        super().__init__(parent, bg="#f0f2f5")
        self.controlador = controlador
        self.servicio = servicio
        self.logo = None

        frame_login = tk.Frame(self, bg="white", padx=35, pady=25, relief="raised", bd=1)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self._cargar_logo(frame_login)

        tk.Label(
            frame_login,
            text="Sistema de Restaurante",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(5, 15))

        tk.Label(frame_login, text="Usuario / Correo:", bg="white", anchor="w").pack(fill="x")
        self.entry_usuario = tk.Entry(frame_login, font=("Arial", 12), width=25)
        self.entry_usuario.pack(pady=5)

        tk.Label(frame_login, text="Contraseña:", bg="white", anchor="w").pack(fill="x")
        self.entry_clave = tk.Entry(frame_login, show="*", font=("Arial", 12), width=25)
        self.entry_clave.pack(pady=5)

        btn_ingresar = tk.Button(
            frame_login,
            text="Ingresar",
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.verificar_login
        )
        btn_ingresar.pack(pady=15, fill="x")

        self.entry_clave.bind("<Return>", lambda event: self.verificar_login())
        self.entry_usuario.focus_set()

    def _cargar_logo(self, contenedor):
        ruta = str(Path(__file__).resolve().parent.parent / "assets" / "logo.png")
        if not os.path.exists(ruta):
            return
        try:
            self.logo = tk.PhotoImage(file=ruta)
            factor = max(1, self.logo.width() // 260)
            if factor > 1:
                self.logo = self.logo.subsample(factor, factor)
            tk.Label(contenedor, image=self.logo, bg="white").pack(pady=(0, 5))
        except tk.TclError:
            pass

    def verificar_login(self):
        correo = self.entry_usuario.get().strip()
        clave = self.entry_clave.get()

        usuario = self.servicio.autenticar_usuario(correo, clave)
        if usuario:
            self.controlador.mostrar_main_view(usuario)
        else:
            messagebox.showerror("Error de acceso", "Credenciales incorrectas. Verifique sus datos.")
