import os
import requests
import mysql.connector

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",     # Cambia esto si tu base de datos está en otro servidor
    user="usuario",          # Cambia esto a tu usuario
    password="usuario",  # Cambia esto a tu contraseña
    database="tienda_juegos"  # Cambia esto al nombre de tu base de datos
)

# Crea un cursor para ejecutar las consultas
cursor = db.cursor()

# Consulta para obtener los links de las imágenes y los nombres de los productos
cursor.execute("SELECT Nombre, Imagen FROM Productos")

# Crea una carpeta para guardar las imágenes si no existe
if not os.path.exists("imagenes_productos"):
    os.makedirs("imagenes_productos")

# Itera sobre los resultados de la consulta
for nombre, imagen_url in cursor.fetchall():
    try:
        # Realiza la solicitud HTTP para obtener la imagen
        response = requests.get(imagen_url)

        # Verifica que la solicitud fue exitosa
        if response.status_code == 200:
            # Guardar la imagen con el nombre del producto
            image_path = os.path.join("imagenes_productos", f"{nombre}.jpg")
            with open(image_path, "wb") as file:
                file.write(response.content)
            print(f"Imagen {nombre} descargada exitosamente.")
        else:
            print(f"No se pudo descargar la imagen de {nombre}, URL no válida.")
    except Exception as e:
        print(f"Error al descargar la imagen de {nombre}: {e}")

# Cierra la conexión a la base de datos
cursor.close()
db.close()
