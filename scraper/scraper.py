import requests as req
from bs4 import BeautifulSoup
import json
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
           }

product = "notebook"
formatted_product = product.replace(" ", "-")

url = f"https://www.amazon.com/s?k={formatted_product}"
product_list = []
max_per_page = 50
page = 1

while True:
    print(f"Scraping page {page}...")
    response = req.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.content, "html.parser")
    product_links = soup.select("li.ui-search-layout__item")
    if not product_links:
        break  # No more products found


    for item in product_links:
        # TODO: finish the scraping logic

