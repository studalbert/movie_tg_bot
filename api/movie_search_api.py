import json
import requests
from config import API_KEY

def movie_search_response_data(count, movie_name):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit={count}&query={movie_name}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return 'Не удалось выполнить поиск'
    else:
        return json.loads(response.text)

