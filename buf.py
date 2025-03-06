import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración inicial del WebDriver
driver = webdriver.Chrome()  # Cambia a tu controlador si es necesario
url = "https://buff.market/market/best_deals?min_price=15"  # Cambia esto por la URL de la página que quieres scrapear
driver.get(url)

# Maximizar la ventana para asegurar visibilidad
driver.maximize_window()

# Esperar hasta que las tarjetas estén visibles
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "goods-card")))

# Obtener todas las tarjetas de productos
goods_cards = driver.find_elements(By.CLASS_NAME, "goods-card")

# Crear o abrir el archivo CSV para escribir los datos
with open('bufmarket.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escribir encabezados en el CSV
    writer.writerow(["ID", "Nombre", "Precio", "URL de la Imagen", "Estado", "Float", "Atributo fijo"])

    # Recorrer las tarjetas y extraer la información deseada
    for idx, card in enumerate(goods_cards, start=1):  # Usamos enumerate para obtener un índice único
        try:
            # Nombre del producto
            name = card.find_element(By.CSS_SELECTOR, "h3 span").text

            # Precio del producto
            raw_price = card.find_element(By.CSS_SELECTOR, "a p.user-price").text
            # Limpiar y convertir el precio a float
            price = float(raw_price.replace('$', '').replace(',', '').strip())

            # URL de la imagen del producto
            img_url = card.find_element(By.CSS_SELECTOR, ".goods-card-img").get_attribute("style")
            img_url = img_url.split('url("')[1].split('")')[0]  # Limpiar la URL

            # Rareza (FT, etc.) - Puede no estar presente en algunos casos
            try:
                rarity = card.find_element(By.CSS_SELECTOR, ".goods-card-tags span[style*='color']").text
            except:
                rarity = "N/A"  # Si no se encuentra rareza, asignar "N/A"

            # Valor adicional (número flotante) - Puede no estar presente en algunos casos
            try:
                additional_value = card.find_element(By.CSS_SELECTOR, ".goods-card-tags span[style*='margin-left']").text
            except:
                additional_value = "N/A"  # Si no se encuentra el valor adicional, asignar "N/A"

            # Si alguna de las propiedades tiene "N/A", omitimos este producto
            if rarity == "N/A" or additional_value == "N/A":
                print(f"Producto omitido debido a valores 'N/A' en 'Estado' o 'Float': {name}")
                continue  # Saltamos a la siguiente tarjeta

            # Atributo fijo
            fixed_attribute = "Buff"

            # Escribir los datos de la tarjeta en el archivo CSV, sin el atributo "Sticker"
            writer.writerow([idx, name, price, img_url, rarity, additional_value, fixed_attribute])

            # Imprimir los datos extraídos (opcional)
            print(f"ID: {idx}")
            print(f"Nombre: {name}")
            print(f"Precio: {price}")
            print(f"URL de la imagen: {img_url}")
            print(f"Estado: {rarity}")
            print(f"Float: {additional_value}")
            print(f"Atributo fijo: {fixed_attribute}")
            print("-" * 50)

        except Exception as e:
            print(f"Error al procesar una tarjeta: {e}")

# Cerrar el navegador al finalizar
driver.quit()
