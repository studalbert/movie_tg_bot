import json

import requests

from config import API_KEY

def movie_by_rating_response_data():
    url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit={data['quantity']}&selectFields=name&selectFields=description&selectFields=year&selectFields=ageRating&selectFields=genres&selectFields=rating&selectFields=poster&selectFields=budget&notNullFields=name&notNullFields=description&notNullFields=rating.kp&notNullFields=poster.url&notNullFields=ageRating&notNullFields=budget.value&sortField=rating.kp&sortType=1&rating.kp={data['movie_rating']}&genres.name={data['genre']}"

    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    response_data = json.loads(response.text)
    return response_data
