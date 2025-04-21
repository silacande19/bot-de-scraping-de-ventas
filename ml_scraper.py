
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import pandas as pd
import os

# Ruta de chromedriver
chromedriver_path = "/Users/mac/Downloads/chromedriver-mac-x64/chromedriver"

# Configuración de Chrome
options = Options()
ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

# Inicializar driver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL de impresión 3D en Mercado Libre
url = 'https://listado.mercadolibre.com.ar/impresion-3d'
driver.get(url)
time.sleep(random.randint(2, 5))  # Espera aleatoria entre 2 y 5 segundos

# Hacer scroll para cargar más productos
for _ in range(3):  # Ajusta el número de scrolls según sea necesario
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(2, 5))  # Espera aleatoria

# Parsear HTML con BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extraer productos (nuevo selector mejorado)
items = soup.select('li.ui-search-layout__item div.ui-search-result__content-wrapper')
print(f"Productos encontrados: {len(items)}")

# Lista para guardar datos
productos = []

for item in items[:20]:  # Cambiá este número si querés más productos
    title = item.select_one('h2.ui-search-item__title')
    price = item.select_one('.price-tag-fraction')
    link = item.select_one('a.ui-search-link')
    sold = item.select_one('span.ui-search-item__group__element')

    if title and price and link:
        titulo = title.text.strip()
        precio = price.text.strip()
        url_producto = link['href'].split("#")[0]
        ventas = sold.text.strip() if sold else "No especificado"

        print(f"{titulo} - ${precio} - {ventas} - {url_producto}")
        productos.append({
            'Producto': titulo,
            'Precio': precio,
            'Ventas': ventas,
            'Link': url_producto
        })

# Cerrar navegador
driver.quit()

# Exportar a CSV
output_path = "/Users/mac/Desktop/impresion3d/productos_3d.csv"
df = pd.DataFrame(productos)
df.to_csv(output_path, index=False)

print(f"\nArchivo CSV guardado en: {output_path}")

# Abrir el archivo CSV automáticamente (solo en Mac)
os.system(f"open {output_path}")

import pandas as pd

df = pd.read_csv("/Users/mac/Desktop/impresion3d/productos_3d.csv")
print(df.head())  # Muestra las primeras 5 filas
