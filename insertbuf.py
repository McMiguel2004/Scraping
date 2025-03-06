import mysql.connector
import csv

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="usuario",  # Cambia esto por tu usuario de MySQL
    password="usuario",  # Cambia esto por tu contraseña de MySQL
    database="tienda_juegos"  # Cambia esto por tu base de datos
)

cursor = conexion.cursor()

# Ruta de los archivos CSV
csv_file_buf = "bufmarket.csv"
csv_file_csfloat = "csfloat.csv"

# Query para insertar datos en la tabla Productos
insert_query = """
INSERT INTO Productos (Nombre, Imagen, Precio, PrecisionValue, Estado, Pagina)
VALUES (%s, %s, %s, %s, %s, %s)
"""

try:
    # Insertar datos desde bufmarket.csv
    with open(csv_file_buf, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Extraer los valores del CSV
            nombre = row["Nombre"]
            imagen = row["URL de la Imagen"]
            precio = float(row["Precio"])
            precision_value = float(row["Float"])
            estado = row["Estado"]
            pagina = row["Atributo fijo"]

            # Insertar en la base de datos (no insertamos el 'id' porque es AUTO_INCREMENT)
            cursor.execute(insert_query, (nombre, imagen, precio, precision_value, estado, pagina))

        print("Datos insertados correctamente desde bufmarket.csv.")

    # Insertar datos desde csfloat.csv
    with open(csv_file_csfloat, mode="r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)

        # Saltar la cabecera del CSV
        next(csvreader)

        for row in csvreader:
            try:
                # Asignar cada valor de la fila a sus correspondientes variables
                nombre = row[1]
                imagen = row[2]
                precio = float(row[3])
                precision_value = float(row[4])
                estado = row[5]
                pagina = row[6]

                # Insertar en la base de datos (no insertamos el 'id' porque es AUTO_INCREMENT)
                cursor.execute(insert_query, (nombre, imagen, precio, precision_value, estado, pagina))
                conexion.commit()  # Confirmar la inserción

                print(f"Datos de '{nombre}' insertados correctamente desde csfloat.csv.")

            except Exception as e:
                print(f"Error al insertar datos desde csfloat.csv: {e}")
                continue

    # Confirmar los cambios al final
    conexion.commit()

except FileNotFoundError as e:
    print(f"Error: {e}")
except mysql.connector.Error as err:
    print(f"Error al interactuar con la base de datos: {err}")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    # Cerrar la conexión
    cursor.close()
    conexion.close()
