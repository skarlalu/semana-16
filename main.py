import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RiquisimO - Restaurante App - Semana 16")
        self.geometry("1050x700")
        self.minsize(900, 620)

        self.servicio = RestauranteServicio()
        self.usuario_actual = None

        self.contenedor = tk.Frame(self, bg="#f5f6fa")
        self.contenedor.pack(fill="both", expand=True)

        self.vista_actual = None
        self.mostrar_login_view()

    def mostrar_login_view(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.usuario_actual = None
        self.vista_actual = LoginView(self.contenedor, self, self.servicio)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_main_view(self, usuario):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.usuario_actual = usuario
        self.vista_actual = MainView(self.contenedor, self, self.servicio, usuario)
        self.vista_actual.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        self.mostrar_login_view()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
