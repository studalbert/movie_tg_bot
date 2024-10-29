import json
from typing import Dict, Any, Union
import requests
from config import API_KEY


def movie_search_response_data(count: str, movie_name: str) -> Union[str, Dict[str, Any]]:
    """
     Функция отправляет запрос на сервер для поиска фильмов по названию.

    :param count: Количество выводимых вариантов (должно быть строкой, представляющей целое число).
    :param movie_name: Название фильма для поиска.
    :return: Словарь с данными о фильмах в случае успешного запроса или строку с сообщением об ошибке.
    """
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
