from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)

# Dane do połączenia się z silnikiem webscraperowym
SCRAPER_URL = 'http://scraper:8000/scrape'

# Dane do połaczenia się z bazą danych
client = MongoClient(host='database', port=27017, username='root', password='pass', authSource="admin")
db = client.mytododb
kolekcja = db.projekt

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Funkcja, która łączy się z silnikiem w celu webscrapowania danych oraz wysyłająca te dane do MongoDB
@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    response = requests.post(SCRAPER_URL, json=data)
    kolekcja.insert_many(response.json())
    return jsonify(response.json())

# Funkcja odnosząca się do podstrony, w której można przeglądywać dane z bazy
@app.route('/data')
def data():
    return render_template('data.html')

# Funkcja, pobierająca dane z bazy, które potem sortuje
@app.route('/get_data', methods=['GET'])
def get_data():
    sort_field = request.args.get('sort', 'title')
    sort_order = request.args.get('order', 'asc')
    search_field = request.args.get('field', None)
    search_value = request.args.get('value', None)
    
    query = {}
    if search_field and search_value:
        if search_field in ['price', 'reviews']:
            try:
                
                search_value = float(search_value) if search_field == 'price' else int(search_value)
                query[search_field] = search_value
            except ValueError:
                return jsonify({'error': 'Invalid search value for numeric field'}), 400
        else:
            query[search_field] = {'$regex': search_value, '$options': 'i'}
    
    
    sort_criteria = [(sort_field, 1 if sort_order == 'asc' else -1)]
    wszystkie_dane = kolekcja.find(query).sort(sort_criteria)
    wynik = json_util.dumps(wszystkie_dane)
    return wynik
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
