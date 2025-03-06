import mysql.connector

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="usuario",
    database="tienda_juegos"
)

cursor = conexion.cursor()

# Crear las tablas necesarias
queries = [
    """
    CREATE TABLE IF NOT EXISTS Usuarios (
        Id INT NOT NULL AUTO_INCREMENT,
        Nombre VARCHAR(255) NOT NULL,
        Contrasena VARCHAR(255) NOT NULL,
        admin TINYINT(1) DEFAULT 0,
        PRIMARY KEY (Id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """,

    """
    CREATE TABLE IF NOT EXISTS Productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Nombre VARCHAR(255) NOT NULL,
        Imagen VARCHAR(500),
        Precio DECIMAL(10, 2),
        PrecisionValue DOUBLE,
        Estado VARCHAR(255),
        Pagina VARCHAR(500),
        FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Compras (
        id_compra INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT,
        id_producto INT,
        fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
        cantidad INT DEFAULT 1,
        estado_compra ENUM('completada', 'pendiente', 'cancelada') DEFAULT 'pendiente',
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(Id) ON DELETE CASCADE,
        FOREIGN KEY (id_producto) REFERENCES Productos(id) ON DELETE CASCADE
    );
    """
]

# Ejecutar las queries para crear las tablas
for query in queries:
    try:
        cursor.execute(query)
        print(f"Tabla creada o verificada correctamente: {query.split()[5]}")
    except mysql.connector.Error as err:
        print(f"Error al ejecutar la query: {err}")

# Función para agregar columna si no existe
def add_column_if_not_exists(table_name, column_name, column_definition):
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
        result = cursor.fetchone()
        if not result:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
            print(f"Columna '{column_name}' añadida a la tabla '{table_name}'.")
        else:
            print(f"La columna '{column_name}' ya existe en la tabla '{table_name}'.")
    except mysql.connector.Error as err:
        print(f"Error al agregar la columna '{column_name}' a la tabla '{table_name}': {err}")

# Llamar a la función para agregar columnas adicionales si se necesitan
add_column_if_not_exists('csfloat', 'FechaCreacion', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
add_column_if_not_exists('buf', 'FechaCreacion', 'DATETIME DEFAULT CURRENT_TIMESTAMP')

# Función para eliminar tablas si existen
def drop_table_if_exists(table_name):
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Tabla '{table_name}' eliminada con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar la tabla '{table_name}': {err}")

# Eliminar tablas no deseadas
drop_table_if_exists('Skin')

# Cerrar conexión
cursor.close()
conexion.close()
print("Base de datos creada y actualizada con éxito.")
