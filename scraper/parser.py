from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup

#Zadaniem tej funkcji jest zwebscraperowanie konkretnych danych z adresu url
def parse_html(html, profile):
    if not html:
        return {}

    #Użycie beautifulsoupa do scraperowania
    soup = BeautifulSoup(html, 'html.parser')

    #Zinicjalizowanie tablicy
    data = []

    #Oddzielenie produktów
    products = soup.select('.thumbnail')
    for product in products:
        product_data = {}
        #Znalezienie nazwy danego produktu
        if profile.get('title'):
            title_elem = product.select_one('.title')
            product_data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'
        
        #Znalezienie ceny danego produktu
        if profile.get('price'):
            price_elem = product.select_one('.price')
            if price_elem:
                price_text = price_elem.get_text(strip=True).replace('$', '').replace(',', '')
                try:
                    product_data['price'] = float(price_text)
                except ValueError:
                    product_data['price'] = 0.0
            else:
                product_data['price'] = 0.0

        #Znalezienie opisu danego produktu
        if profile.get('description'):
            desc_elem = product.select_one('.description')
            product_data['description'] = desc_elem.get_text(strip=True) if desc_elem else 'N/A'

        #Wyliczenie ile gwiazdek ma dany produkt
        if profile.get('rating'):
            rating_elems = product.select("span.ws-icon.ws-icon-star")
            rating_text = str(len(rating_elems))+'/4' if rating_elems else 'N/A'
            product_data['rating'] = rating_text
        
        #Znalezienie ile opinii ma dany produkt
        if profile.get('reviews'):
            review_elem = product.select_one('.review-count')
            if review_elem:
                review_text = review_elem.get_text(strip=True).split()[0]
                try:
                    product_data['reviews'] = int(review_text)
                except ValueError:
                    product_data['reviews'] = 0
            else:
                product_data['reviews'] = 0

        #Dodanie danych do tablicy   
        data.append(product_data)

    return data

#Zadaniem tej funkcji jest wykonanie przetwarzania wieloprocesowego funkcji podanej powyżej, ze skalowaniem na rdzenie procesora
def process_data(html_list, profile):
    with Pool(cpu_count()) as pool:
        results = pool.starmap(parse_html, [(html, profile) for html in html_list if html is not None])
    #Scalenie listy list w jedną listę
    flattened_results = [item for sublist in results for item in sublist]
    return flattened_results
