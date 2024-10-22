import json
import requests
from config import API_KEY

def low_budget_movie_response_data():
    url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit={data['quantity']}&selectFields=name&selectFields=description&selectFields=budget&selectFields=rating&selectFields=ageRating&selectFields=genres&selectFields=poster&selectFields=year&notNullFields=name&notNullFields=description&notNullFields=year&notNullFields=ageRating&notNullFields=budget.value&sortField=budget.value&sortType=1&genres.name={data['genre']}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    return response_data