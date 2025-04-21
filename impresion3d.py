
# impresion3d.py

import requests
from bs4 import BeautifulSoup

# URL de búsqueda en Mercado Libre Argentina
url = "https://listado.mercadolibre.com.ar/impresora-3d"

# Headers para simular navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Solicitud HTTP
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Buscar los productos
    productos = soup.select("li.ui-search-layout__item")

    if not productos:
        print("⚠️ No se encontraron productos. Mercado Libre podría haber cambiado su estructura.")
    
    for producto in productos:
        titulo = producto.select_one("h2.ui-search-item__title")
        precio = producto.select_one("span.andes-money-amount__fraction")
        link = producto.select_one("a.ui-search-link")

        if titulo and precio and link:
            print("🛒 Producto:", titulo.text.strip())
            print("💰 Precio: $", precio.text.strip())
            print("🔗 Link:", link["href"])
            print("-" * 60)
else:
    print("❌ Error al acceder a Mercado Libre. Código HTTP:", response.status_code)


with open("resultado.html", "w", encoding="utf-8") as f:
    f.write(response.text)

