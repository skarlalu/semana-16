Estudiante: Karla Daniela Luque Navarrete

Aplicación gráfica de gestión para un restaurante, desarrollada como evolución del proyecto de las semanas anteriores de Programación Orientada a Objetos.

Objetivo de la Semana 16

La Semana 16 continúa el proyecto de la Semana 15 y aplica el manejo de eventos de Tkinter a la gestión de usuarios. Se conserva la arquitectura modular, la persistencia mediante archivos JSON, el inicio de sesión, productos, ventas y los recursos visuales de `assets/`.

La principal evolución consiste en convertir la sección de Usuarios en una gestión CRUD con roles básicos y eventos mediante `bind()`.

Funcionalidades

- Inicio de sesión con identificación del usuario autenticado y su rol.
- Gestión de productos: registrar, consultar, actualizar y eliminar.
- Gestión administrativa de usuarios disponible únicamente para el rol **Administrador**.
- Registro, consulta, actualización y eliminación de usuarios.
- Roles: **Administrador, Empleado y Cliente**.
- Visualización de usuarios mediante `Treeview` sin mostrar contraseñas.
- Persistencia de usuarios en `datos/usuarios.json`.
- Registro de ventas relacionando un usuario existente con un producto existente.
- Persistencia de ventas en `datos/ventas.json`.
- Logo e íconos integrados desde `assets/`.

El sistema maneja tres roles básicos:

- **Administrador:** puede acceder a la pestaña Usuarios y gestionar cuentas.
- **Empleado:** puede utilizar las funciones generales disponibles, pero no accede a la gestión administrativa de usuarios.
- **Cliente:** puede utilizar las funciones generales disponibles, pero no accede a la gestión administrativa de usuarios.

La cuenta administrativa actualmente autenticada no puede eliminarse accidentalmente. Tampoco puede cambiarse su rol a un rol diferente mientras se encuentra autenticada.

Separación de responsabilidades

La interfaz captura eventos, obtiene datos de los controles y actualiza la vista. Las validaciones, reglas de negocio y persistencia permanecen en `RestauranteServicio`.
