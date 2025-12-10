# 📦 Sistema de Gestión de Inventario (Python/SQLite)

Este proyecto es una aplicación de consola para la gestión de inventario, desarrollada en Python, que utiliza la librería estándar `sqlite3` para el almacenamiento persistente de los datos de productos. La interfaz de usuario es interactiva y utiliza colores para mejorar la experiencia en la terminal.

---

## 🚀 Características y Funcionalidades

El sistema ofrece las siguientes opciones de gestión de inventario:

1.  **Registrar Producto:** Añadir un nuevo artículo al inventario.
2.  **Visualizar Inventario:** Mostrar todos los productos registrados en una tabla legible.
3.  **Actualizar Producto:** Modificar los datos de un producto existente usando su ID.
4.  **Eliminar Producto:** Eliminar un artículo del inventario por su ID.
5.  **Buscar Producto:** Búsqueda por ID, Nombre o Categoría.
6.  **Reporte de Stock Bajo:** Generar un reporte de productos cuya cantidad esté por debajo de un umbral específico.

---

## 🛠️ Requisitos del Sistema

Para ejecutar esta aplicación, solo necesitas tener instalado Python y las siguientes librerías:

* **Python 3.x**
* **`colorama`**: Para la gestión de colores en la terminal.
* **`sqlite3`**: (Módulo estándar de Python, no requiere instalación adicional).

### Instalación de Dependencias

Puedes instalar la librería `colorama` usando `pip`:

```bash
pip install colorama
