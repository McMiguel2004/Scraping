import pymysql
import requests
import os

# Datos de conexión a la base de datos
DB_HOST = "localhost"
DB_NAME = "tienda_juegos"
DB_USER = "usuario"
DB_PASS = "usuario"

# Carpeta donde se guardarán las imágenes
IMG_FOLDER = "imagenes_productos"
os.makedirs(IMG_FOLDER, exist_ok=True)

# Conectar a la base de datos
try:
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cursor = connection.cursor()

    # Consultar los productos
    cursor.execute("SELECT Nombre, Imagen FROM Productos")
    productos = cursor.fetchall()

    for nombre, url in productos:
        if not url:
            continue  # Saltar si no hay URL de imagen

        # Formatear el nombre del archivo
        nombre_archivo = nombre.replace(" | ", "_").replace(" ", "_").replace("'", "").replace("\"", "") + ".png"
        ruta_guardado = os.path.join(IMG_FOLDER, nombre_archivo)

        try:
            # Descargar la imagen
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(ruta_guardado, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Imagen guardada: {ruta_guardado}")
            else:
                print(f"No se pudo descargar la imagen de {nombre} - Código: {response.status_code}")
        except Exception as e:
            print(f"Error al descargar {url}: {e}")

    # Cerrar conexión
    cursor.close()
    connection.close()
    print("Proceso finalizado.")

except pymysql.MySQLError as e:
    print(f"Error de conexión a la base de datos: {e}")
