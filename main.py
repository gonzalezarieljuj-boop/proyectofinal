import database_manager as db
import os # Para limpiar la consola (cls/clear)
from colorama import Fore, Style, init # Opcional: para colores en la terminal 

# Inicializa colorama (solo necesario si se usa)
try:
    init(autoreset=True)
    USE_COLORAMA = True
except ImportError:
    USE_COLORAMA = False
    
# --- Funciones de Utilidad de Interfaz ---

def clear_screen():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_table(productos):
    """Imprime la lista de productos en formato de tabla legible."""
    if not productos:
        print(Fore.YELLOW + "\n[!] No se encontraron productos." if USE_COLORAMA else "\n[!] No se encontraron productos.")
        return

    # Definición de anchos de columna para formato fijo
    ID_W, NOMBRE_W, DESCRIPCION_W, CANTIDAD_W, PRECIO_W, CATEGORIA_W = 4, 20, 30, 10, 8, 15

    # Cabecera de la tabla
    header = (
        f"{'ID':<{ID_W}} | "
        f"{'NOMBRE':<{NOMBRE_W}} | "
        f"{'DESCRIPCIÓN':<{DESCRIPCION_W}} | "
        f"{'CANT.':<{CANTIDAD_W}} | "
        f"{'PRECIO':<{PRECIO_W}} | "
        f"{'CATEGORÍA':<{CATEGORIA_W}}"
    )
    
    separator = "-" * len(header)
    
    print("\n" + Fore.CYAN + separator if USE_COLORAMA else "\n" + separator)
    print(Fore.CYAN + header if USE_COLORAMA else header)
    print(Fore.CYAN + separator if USE_COLORAMA else separator)

    # Cuerpo de la tabla
    for p in productos:
        # Los objetos Row de SQLite permiten acceder por nombre de columna
        row = (
            f"{p['id']:<{ID_W}} | "
            f"{p['nombre'][:NOMBRE_W]:<{NOMBRE_W}} | "
            f"{p['descripcion'][:DESCRIPCION_W]:<{DESCRIPCION_W}} | "
            f"{p['cantidad']:<{CANTIDAD_W}} | "
            f"{p['precio']:<{PRECIO_W}.2f} | " # Formatear precio a 2 decimales
            f"{p['categoria'][:CATEGORIA_W]:<{CATEGORIA_W}}"
        )
        print(row)
        
    print(Fore.CYAN + separator + "\n" if USE_COLORAMA else separator + "\n")

# --- Funcionalidades Requeridas (Interfaz) ---

def menu_registrar_producto():
    """Permite al usuario ingresar datos para un nuevo producto."""
    print(Fore.YELLOW + "\n--- Registrar Nuevo Producto ---" if USE_COLORAMA else "\n--- Registrar Nuevo Producto ---")
    
    # 1. Solicitar y validar nombre (NO NULL)
    nombre = input("Nombre del Producto (Obligatorio): ").strip()
    if not nombre:
        print(Fore.RED + "El nombre es obligatorio. Operación cancelada." if USE_COLORAMA else "El nombre es obligatorio. Operación cancelada.")
        return

    descripcion = input("Descripción (Opcional): ").strip()

    # 2. Solicitar y validar cantidad (INTEGER, NO NULL)
    try:
        cantidad = int(input("Cantidad Disponible (Obligatorio): "))
        if cantidad < 0: raise ValueError
    except ValueError:
        print(Fore.RED + "Cantidad debe ser un número entero positivo. Operación cancelada." if USE_COLORAMA else "Cantidad debe ser un número entero positivo. Operación cancelada.")
        return

    # 3. Solicitar y validar precio (REAL, NO NULL)
    try:
        precio = float(input("Precio (Obligatorio): "))
        if precio <= 0: raise ValueError
    except ValueError:
        print(Fore.RED + "Precio debe ser un número real positivo. Operación cancelada." if USE_COLORAMA else "Precio debe ser un número real positivo. Operación cancelada.")
        return

    categoria = input("Categoría (Opcional): ").strip()

    # 4. Llamar a la función de la base de datos
    if db.registrar_producto(nombre, descripcion, cantidad, precio, categoria):
        print(Fore.GREEN + f"✅ Producto '{nombre}' registrado con éxito." if USE_COLORAMA else f"✅ Producto '{nombre}' registrado con éxito.")
    else:
        print(Fore.RED + "❌ Error al registrar el producto." if USE_COLORAMA else "❌ Error al registrar el producto.")

def menu_visualizar_productos():
    """Muestra todos los productos registrados en una tabla."""
    print(Fore.YELLOW + "\n--- Inventario Completo ---" if USE_COLORAMA else "\n--- Inventario Completo ---")
    productos = db.visualizar_productos() 
    print_table(productos)

def menu_actualizar_producto():
    """Permite al usuario actualizar los datos de un producto por ID."""
    print(Fore.YELLOW + "\n--- Actualizar Producto por ID ---" if USE_COLORAMA else "\n--- Actualizar Producto por ID ---")
    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        print(Fore.RED + "El ID debe ser un número entero." if USE_COLORAMA else "El ID debe ser un número entero.")
        return
        
    # Opcional: Mostrar el producto actual antes de actualizar
    productos_encontrados = db.buscar_producto('id', id_producto)
    if not productos_encontrados:
        print(Fore.RED + f"No se encontró ningún producto con ID {id_producto}." if USE_COLORAMA else f"No se encontró ningún producto con ID {id_producto}.")
        return
        
    # Obtener los datos actuales para usar como valores por defecto
    producto_actual = productos_encontrados[0]
    
    print(Fore.CYAN + "\n--- Datos Actuales ---" if USE_COLORAMA else "\n--- Datos Actuales ---")
    print_table(productos_encontrados)
    
    # Pedir nuevos datos (dejar vacío para mantener el valor actual)
    print(Fore.CYAN + "Ingrese los nuevos valores o presione ENTER para mantener el valor actual entre [corchetes]:" if USE_COLORAMA else "Ingrese los nuevos valores o presione ENTER para mantener el valor actual entre [corchetes]:")

    nombre = input(f"Nombre [{producto_actual['nombre']}]: ").strip() or producto_actual['nombre']
    if not nombre:
         print(Fore.RED + "El nombre es obligatorio. Operación cancelada." if USE_COLORAMA else "El nombre es obligatorio. Operación cancelada.")
         return
         
    descripcion = input(f"Descripción [{producto_actual['descripcion']}]: ").strip() or producto_actual['descripcion']
    
    while True:
        cantidad_str = input(f"Cantidad [{producto_actual['cantidad']}]: ").strip()
        if not cantidad_str:
            cantidad = producto_actual['cantidad']
            break
        try:
            cantidad = int(cantidad_str)
            if cantidad < 0: raise ValueError
            break
        except ValueError:
            print(Fore.RED + "Cantidad debe ser un número entero positivo." if USE_COLORAMA else "Cantidad debe ser un número entero positivo.")
            
    while True:
        precio_str = input(f"Precio [{producto_actual['precio']}]: ").strip()
        if not precio_str:
            precio = producto_actual['precio']
            break
        try:
            precio = float(precio_str)
            if precio <= 0: raise ValueError
            break
        except ValueError:
            print(Fore.RED + "Precio debe ser un número real positivo." if USE_COLORAMA else "Precio debe ser un número real positivo.")
            
    categoria = input(f"Categoría [{producto_actual['categoria']}]: ").strip() or producto_actual['categoria']

    # Llamar a la función de la base de datos
    if db.actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
        print(Fore.GREEN + f"✅ Producto con ID {id_producto} actualizado con éxito." if USE_COLORAMA else f"✅ Producto con ID {id_producto} actualizado con éxito.")
    else:
        print(Fore.RED + f"❌ Error al actualizar o no se encontró el producto con ID {id_producto}." if USE_COLORAMA else f"❌ Error al actualizar o no se encontró el producto con ID {id_producto}.")

def menu_eliminar_producto():
    """Permite al usuario eliminar un producto por ID."""
    print(Fore.YELLOW + "\n--- Eliminar Producto por ID ---" if USE_COLORAMA else "\n--- Eliminar Producto por ID ---")
    try:
        id_producto = int(input("Ingrese el ID del producto a eliminar: "))
    except ValueError:
        print(Fore.RED + "El ID debe ser un número entero." if USE_COLORAMA else "El ID debe ser un número entero.")
        return
        
    # Confirmación
    confirm = input(f"¿Está seguro que desea eliminar el producto con ID {id_producto}? (s/N): ").lower()
    if confirm != 's':
        print(Fore.YELLOW + "Operación de eliminación cancelada." if USE_COLORAMA else "Operación de eliminación cancelada.")
        return

    if db.eliminar_producto(id_producto):
        print(Fore.GREEN + f"✅ Producto con ID {id_producto} eliminado con éxito." if USE_COLORAMA else f"✅ Producto con ID {id_producto} eliminado con éxito.")
    else:
        print(Fore.RED + f"❌ No se encontró o no se pudo eliminar el producto con ID {id_producto}." if USE_COLORAMA else f"❌ No se encontró o no se pudo eliminar el producto con ID {id_producto}.")

def menu_buscar_producto():
    """Permite al usuario buscar productos por varios criterios."""
    print(Fore.YELLOW + "\n--- Búsqueda de Productos ---" if USE_COLORAMA else "\n--- Búsqueda de Productos ---")
    print("Buscar por:")
    print("1. ID") 
    print("2. Nombre") 
    print("3. Categoría") 
    
    opcion = input("Seleccione una opción de búsqueda (1-3): ").strip()
    valor_busqueda = input("Ingrese el valor a buscar: ").strip()
    
    criterio_map = {
        '1': 'id',
        '2': 'nombre',
        '3': 'categoria'
    }
    
    criterio = criterio_map.get(opcion)
    
    if not criterio or not valor_busqueda:
        print(Fore.RED + "Opción o valor de búsqueda no válidos." if USE_COLORAMA else "Opción o valor de búsqueda no válidos.")
        return
        
    # Llamar a la función de búsqueda
    productos_encontrados = db.buscar_producto(criterio, valor_busqueda)
    print(Fore.CYAN + f"\nResultados de la búsqueda por {criterio} = '{valor_busqueda}':" if USE_COLORAMA else f"\nResultados de la búsqueda por {criterio} = '{valor_busqueda}':")
    print_table(productos_encontrados)

def menu_reporte_stock():
    """Genera un reporte de productos con stock bajo."""
    print(Fore.YELLOW + "\n--- Reporte de Productos con Stock Bajo ---" if USE_COLORAMA else "\n--- Reporte de Productos con Stock Bajo ---")
    try:
        limite = int(input("Mostrar productos con Cantidad igual o inferior a (Límite): "))
        if limite < 0: raise ValueError
    except ValueError:
        print(Fore.RED + "El límite debe ser un número entero positivo." if USE_COLORAMA else "El límite debe ser un número entero positivo.")
        return
        
    productos = db.reporte_bajo_stock(limite)
    
    print(Fore.CYAN + f"\n--- Productos con Stock <= {limite} ---" if USE_COLORAMA else f"\n--- Productos con Stock <= {limite} ---")
    print_table(productos)


# --- Menú Principal y Bucle de Aplicación ---

def mostrar_menu():
    """Muestra el menú principal de la aplicación."""
    clear_screen()
    
    if USE_COLORAMA:
        print(Fore.GREEN + Style.BRIGHT + "================================================")
        print("  SISTEMA DE GESTIÓN DE INVENTARIO (Python/SQLite)")
        print("================================================" + Style.RESET_ALL)
        print(Fore.YELLOW + "\n--- MENÚ PRINCIPAL ---")
        print(Fore.CYAN + "1." + Fore.WHITE + " Registrar nuevo producto")
        print(Fore.CYAN + "2." + Fore.WHITE + " Visualizar inventario completo")
        print(Fore.CYAN + "3." + Fore.WHITE + " Actualizar producto (por ID)")
        print(Fore.CYAN + "4." + Fore.WHITE + " Eliminar producto (por ID)")
        print(Fore.CYAN + "5." + Fore.WHITE + " Buscar producto")
        print(Fore.CYAN + "6." + Fore.WHITE + " Reporte de productos con stock bajo")
        print(Fore.RED + "7." + Fore.WHITE + " Salir")
        print(Fore.GREEN + "------------------------------------------------" + Style.RESET_ALL)
    else:
        # Versión sin colores
        print("================================================")
        print("  SISTEMA DE GESTIÓN DE INVENTARIO (Python/SQLite)")
        print("================================================")
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar nuevo producto")
        print("2. Visualizar inventario completo")
        print("3. Actualizar producto (por ID)")
        print("4. Eliminar producto (por ID)")
        print("5. Buscar producto")
        print("6. Reporte de productos con stock bajo")
        print("7. Salir")
        print("------------------------------------------------")

def main():
    """Bucle principal de la aplicación."""
    # Inicializa la base de datos (crea el archivo/tabla si no existen)
    db.setup_database()

    while True:
        mostrar_menu()
        
        opcion = input("Ingrese su opción (1-7): ").strip()
        
        if opcion == '1':
            menu_registrar_producto()
        elif opcion == '2':
            menu_visualizar_productos()
        elif opcion == '3':
            menu_actualizar_producto()
        elif opcion == '4':
            menu_eliminar_producto()
        elif opcion == '5':
            menu_buscar_producto()
        elif opcion == '6':
            menu_reporte_stock()
        elif opcion == '7':
            print(Fore.YELLOW + "Saliendo de la aplicación. ¡Hasta luego!" if USE_COLORAMA else "Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción no válida. Intente de nuevo." if USE_COLORAMA else "Opción no válida. Intente de nuevo.")
            
        # Esperar la pulsación de una tecla para continuar
        if opcion != '7':
            input("\nPresione ENTER para volver al menú...")


if __name__ == '__main__':
    main()