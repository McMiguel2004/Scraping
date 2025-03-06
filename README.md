Proyecto de Scraping y Gestión de Datos

Este proyecto realiza scraping de datos desde varias fuentes y los almacena en una base de datos MySQL. Luego, permite la descarga automática de imágenes relacionadas para su uso en la web.

📌 Tecnologías utilizadas

Python para el scraping y manipulación de datos.

Selenium para la automatización del navegador.

MySQL para la base de datos.

CSV para el almacenamiento intermedio de datos.

📂 Estructura del proyecto

📁 proyecto_scraping
├── config.py       # Configuración y creación de la base de datos
├── buf.py          # Scraping de la primera página
├── csfloat.py      # Scraping de la segunda página
├── inserts.py      # Inserción de datos en MySQL
├── fotos.py        # Descarga de imágenes desde la base de datos
├── requirements.txt # Dependencias del proyecto
└── README.md       # Documentación del proyecto

⚙️ Instalación y configuración

1️⃣ Clonar el repositorio

git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

2️⃣ Instalar dependencias

pip install -r requirements.txt

3️⃣ Configurar la base de datos

Ejecuta config.py para crear la base de datos y las tablas necesarias:

python config.py

🔍 Proceso de Scraping

4️⃣ Realizar el scraping

Ejecutar buf.py y csfloat.py para extraer los datos:

python buf.py
python csfloat.py

Esto generará archivos CSV con los datos scrapeados.

5️⃣ Insertar datos en MySQL

Ejecutar inserts.py para insertar los datos en la base de datos:

python inserts.py

6️⃣ Descargar imágenes automáticamente

Ejecutar fotos.py para descargar las imágenes asociadas a los productos:

python fotos.py

Las imágenes se guardarán con el nombre del arma correspondiente.

🚀 Despliegue

Una vez realizados los pasos anteriores, los datos estarán listos para ser usados en la web. Puedes conectarte a la base de datos y mostrar los productos con sus imágenes de manera dinámica.

🛠 Requisitos

Python 3.8+

MySQL

Navegador compatible con Selenium (Chrome recomendado)

📜 Licencia

Este proyecto está bajo la licencia MIT.

