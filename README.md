

# Projekt PRiR Autor: Filip Kłos 20453
Zadaniem tego projektu jest webscraperowanie danych adresów url, przez interfejs graficzny flask, a następnie wysłanie tych danych do osobnego kontenera,
który jest bazą MongoDB. Podany webscraper jest przystosowany do pobierania danych z serwisów w których kupuje się produkty
### Przykładowe strony które, używałem do webscraperowania
- https://webscraper.io/test-sites/e-commerce/allinone/phones/touch
- https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets
- https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops

## Struktura katalogów
- `docker-compose.yml`: Plik konfiguracyjny Docker Compose.
- `flask_app/`: Katalog z aplikacją Flask.
  - `app.py`: Główny plik aplikacji Flask.
  - `dockerfile`: Plik Dockerfile dla aplikacji Flask.
  - `requirements.txt`: Lista zależności dla aplikacji Flask.
  - `static/`: Katalog z plikiem CSS.
  - `templates/`: Katalog z szablonami HTML.
- `scraper/`: Katalog z skryptami scraper.
  - `fetcher.py`: Skrypt do pobierania danych.
  - `main.py`: Główny plik scraper.
  - `parser.py`: Skrypt do parsowania danych.
  - `requirements.txt`: Lista zależności dla silnika scraperowego.

## Wymagania
1. Docker
2. Docker-compose
3. Python 3.8+

## Jak uruchomić
1. Uruchom Docker Compose:
   ```sh
   docker-compose up --build
