import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

# Entrada do usuário
search_query = input("Digite o produto que deseja buscar no Mercado Livre: ").strip()
formatted_query = search_query.replace(" ", "-").lower()

base_url = f"https://lista.mercadolivre.com.br/{formatted_query}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

product_list = []
page = 1
max_products = 500  # Limite de produtos

while len(product_list) < max_products:
    print(f"🔎 Buscando página {page}...")

    url = f"{base_url}_Desde_{(page - 1) * 50 + 1}" if page > 1 else base_url
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar a página: {url}")
        break

    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.select('li.ui-search-layout__item')

    if not items:
        print("Nenhum item encontrado ou fim dos resultados.")
        break

    for item in tqdm(items, desc=f"Página {page}", unit="produto"):
        if len(product_list) >= max_products:
            break  # Sai do loop se já atingiu o limite

        title_tag = item.select_one('h2.ui-search-item__title')
        price_tag = item.select_one('span.andes-money-amount__fraction')
        cents_tag = item.select_one('span.andes-money-amount__cents')
        link_tag = item.select_one('a.ui-search-link')

        title = title_tag.get_text(strip=True) if title_tag else 'Sem título'
        price = price_tag.get_text(strip=True) if price_tag else '0'
        cents = cents_tag.get_text(strip=True) if cents_tag else '00'
        full_price = float(f"{price}.{cents}".replace('.', '').replace(',', '.'))

        link = link_tag['href'].split("#")[0] if link_tag else 'Sem link'

        product_list.append({
            "title": title,
            "price": full_price,
            "link": link
        })

    # Se atingiu o limite durante a página atual
    if len(product_list) >= max_products:
        break

    # Verifica se há próxima página
    next_page = soup.select_one('li.andes-pagination__button--next a')
    if not next_page:
        break

    page += 1
    time.sleep(1.5)  # Evita sobrecarregar o site

# Salva em CSV
df = pd.DataFrame(product_list)
df.to_csv("products_scraped_meli.csv", index=False, encoding='utf-8', sep=';')

print("✅ Scraping finalizado!")
print(f"Total de produtos extraídos: {len(product_list)}")
