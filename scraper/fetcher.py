import aiohttp
import asyncio

#Zadaniem tej funkcji jest pobranie treści z konkretnego adresu url
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

#Zadaniem tej funkcji jest tworzenie zadań do zbierania treści z adresów funkcją podaną wyżej oraz wykonanie ich asynchronicznie
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
