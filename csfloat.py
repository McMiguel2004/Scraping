from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configuración del WebDriver
driver = webdriver.Chrome()  # Asegúrate de que ChromeDriver está configurado correctamente
url = "https://csfloat.com/"  # Cambia esto por tu URL real
driver.get(url)

# Maximizar la ventana para asegurar que los elementos sean visibles
driver.maximize_window()

# Desactivar animaciones (si es necesario)
driver.execute_script("""
    document.body.style.animation = 'none';
    document.body.style.transition = 'none';
""")

# Crear o abrir el archivo CSV
csv_filename = "csfloat.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
    # Configurar el escritor de CSV
    csvwriter = csv.writer(csvfile)
    # Escribir la cabecera del archivo CSV con el nuevo orden
    csvwriter.writerow(["Nº", "Nombre", "Imagen", "Precio", "Float", "Estado", "Pagina"])

    # Inicializar el contador
    item_count = 0

    # Función para limpiar nombres
    def clean_name(name):
        # Remover caracteres indeseados como ★ y *
        return name.replace("★", "").replace("*", "").strip()

    # Función para limpiar y convertir el precio a número (float)
    def clean_price(price):
        # Remover el símbolo de moneda y las comas
        price = price.replace("€", "").replace(",", "").strip()

        try:
            # Convertir el precio a float
            return float(price)
        except ValueError:
            # Si no se puede convertir, devolver un valor flotante nulo (None)
            return None

    # Esperar a que el primer botón esté disponible y visible
    try:
        # Esperar que el primer botón sea clickeable
        first_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mat-mdc-button-touch-target"))
        )

        # Hacer scroll al primer botón para asegurarse de que está visible
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_element)
        time.sleep(1)  # Esperar para que el scroll se realice completamente

        # Usar ActionChains para hacer clic en el primer botón
        actions = ActionChains(driver)
        actions.move_to_element(first_element).click().perform()

        print("Primer botón clickeado exitosamente.")

        # Esperar a que las cartas de los items estén disponibles
        item_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item-card'))
        )

        print(f"Se han encontrado {len(item_cards)} cartas.")

        # Iterar sobre cada carta y extraer información
        for item_card in item_cards:
            try:
                # Incrementar el contador
                item_count += 1

                # Asegurarse de que la carta sea clickeable (en caso de que no se haya cargado correctamente)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(item_card))

                # Hacer scroll a la carta para asegurarse de que está visible
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item_card)
                time.sleep(1)  # Esperar para que el scroll se realice completamente

                # Extraer nombre, descripción y precio del item de manera genérica
                item_name = clean_name(item_card.find_element(By.CSS_SELECTOR, '.item-name').text)
                item_subtext = item_card.find_element(By.CSS_SELECTOR, '.subtext').text  # Aquí es donde se obtiene el estado
                price = item_card.find_element(By.CSS_SELECTOR, '.price').text
                cleaned_price = clean_price(price)  # Limpiar y convertir el precio

                # Extraer el valor de wear y paint-seed
                try:
                    wear_value = item_card.find_element(By.CLASS_NAME, 'wear').text
                except:
                    wear_value = "No disponible"

                try:
                    paint_seed_value = item_card.find_element(By.CLASS_NAME, 'paint-seed').text
                except:
                    paint_seed_value = "No disponible"

                # Extraer la URL de la imagen
                try:
                    image_url = item_card.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                except:
                    image_url = "No disponible"

                # Valor fijo para el atributo
                fixed_attribute = "csfloat"

                # Escribir los datos de la carta en el archivo CSV con el nuevo orden
                csvwriter.writerow([item_count, item_name, image_url, cleaned_price, wear_value, item_subtext, fixed_attribute])  # Cambié el "URL de la imagen" por "Imagen"

                # Imprimir para seguimiento en consola
                print(f"Nº {item_count}: Datos de '{item_name}' guardados en el archivo CSV.")

            except Exception as e:
                print(f"Error al intentar interactuar con una carta: {e}")
                continue  # Continuar con la siguiente carta

    except Exception as e:
        print(f"Error al intentar obtener el primer botón o las cartas: {e}")

# No cerrar automáticamente el navegador
driver.quit()  # Comentado para mantener el navegador abierto
