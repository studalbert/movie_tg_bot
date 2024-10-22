import json

import requests

from config import API_KEY

def movie_search_response_data():
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit={data['quantity']}&query={data['movie_name']}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    return response_data