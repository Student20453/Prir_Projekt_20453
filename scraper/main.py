from aiohttp import web
from fetcher import fetch_all
from parser import process_data
import asyncio

#Funkcja główna w silniku scrapera
async def handle_scrape(request):
    try:
        #Przyjęcie danych z kontenera Flaska
        data = await request.json()
        urls = data.get('urls', [])
        profile = data.get('profile', {})
        html_list = await fetch_all(urls)
        #Zescraperowanie danych
        result_data = process_data(html_list, profile)
        #Wysłanie wyniku scraperowania
        return web.json_response(result_data)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_post('/scrape', handle_scrape)

if __name__ == '__main__':
    web.run_app(app, port=8000)
    while True:
        pass
