import sqlite3

# Requisito: Nombre de la base de datos 'inventario.db' [cite: 9, 10]
DB_NAME = 'inventario.db'

# --- Funciones de Utilidad de Conexión ---

def get_db_connection():
    """Retorna un objeto de conexión SQLite."""
    conn = sqlite3.connect(DB_NAME)
    # Habilitar el acceso a las columnas por nombre (útil para la visualización)
    conn.row_factory = sqlite3.Row
    return conn

# --- Funciones CRUD y Setup ---
def setup_database(): # ¡ESTA DEBE SER LA DEFINICIÓN EXACTA!
    """
    Se conecta a la BD y crea la tabla 'productos' si no existe.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Creación de la tabla 'productos' con las columnas requeridas [cite: 11]
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único [cite: 13]
                nombre TEXT NOT NULL,                 -- Nombre del producto (no nulo) [cite: 14]
                descripcion TEXT,                     -- Breve descripción [cite: 15, 16]
                cantidad INTEGER NOT NULL,            -- Cantidad (entero, no nulo) [cite: 17, 18]
                precio REAL NOT NULL,                 -- Precio (real, no nulo) [cite: 19]
                categoria TEXT                        -- Categoría del producto [cite: 20, 21]
            )
        ''')
        
        conn.commit()
        # Nota: En una aplicación real, esto solo se ejecutaría al inicio.
        # print("Base de datos inicializada correctamente.")
        
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    """
    Inserta un nuevo producto en la tabla 'productos'. [cite: 29, 30]
    Retorna True si la inserción fue exitosa, False en caso contrario.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para insertar el nuevo registro
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Esto capturaría errores como 'nombre' siendo NULL (aunque ya lo validaremos)
        print("Error: El producto no se pudo registrar. Verifique los campos obligatorios.")
        return False
    except sqlite3.Error as e:
        print(f"Error de BD al registrar: {e}")
        return False
    finally:
        if conn:
            conn.close()

def visualizar_productos():
    """
    Obtiene y retorna todos los productos registrados. [cite: 31, 32]
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id")
        # El uso de 'conn.row_factory = sqlite3.Row' permite iterar sobre los resultados 
        # como diccionarios, lo que es útil para imprimir.
        productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        print(f"Error de BD al visualizar productos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
    """
    Actualiza los datos de un producto específico mediante su ID. [cite: 33]
    Retorna True si se actualizó al menos un registro.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para actualizar. Usamos WHERE id = ? para asegurar la actualización 
        # solo al producto específico.
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? 
            WHERE id = ?
        ''', (nombre, descripcion, cantidad, precio, categoria, id_producto))
        
        conn.commit()
        # Verificar si se actualizó algún registro
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error de BD al actualizar: {e}")
        return False
    finally:
        if conn:
            conn.close()

def eliminar_producto(id_producto):
    """
    Elimina un producto mediante su ID. [cite: 34]
    Retorna True si se eliminó al menos un registro.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para eliminar el producto
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        
        conn.commit()
        # rowcount indica el número de filas afectadas
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error de BD al eliminar: {e}")
        return False
    finally:
        if conn:
            conn.close()

def buscar_producto(criterio, valor):
    """
    Busca productos por ID, nombre o categoría. [cite: 35]
    Retorna una lista de productos encontrados.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sanitización básica del criterio para evitar inyección SQL en la cláusula del campo
        if criterio not in ['id', 'nombre', 'categoria']:
            print("Criterio de búsqueda no válido.")
            return []
            
        # Sentencia SQL con LIKE para búsquedas parciales en texto, e = ? para ID
        if criterio == 'id':
            query = f"SELECT * FROM productos WHERE {criterio} = ?"
            # El ID debe ser un valor exacto
            cursor.execute(query, (valor,))
        else:
            query = f"SELECT * FROM productos WHERE {criterio} LIKE ?"
            # Se usa % para permitir la búsqueda por subcadena
            cursor.execute(query, (f'%{valor}%',))
            
        productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        print(f"Error de BD al buscar: {e}")
        return []
    finally:
        if conn:
            conn.close()

def reporte_bajo_stock(limite):
    """
    Genera un reporte de productos cuya cantidad es igual o inferior al límite. [cite: 36]
    Retorna una lista de productos con stock bajo.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para encontrar productos donde cantidad <= limite
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC", (limite,))
        
        productos = cursor.fetchall()
        return productos
    except sqlite3.Error as e:
        print(f"Error de BD al generar reporte: {e}")
        return []
    finally:
        if conn:
            conn.close()