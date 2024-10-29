import json
from typing import Dict, Any, Union
import requests
from config import API_KEY, URL


def low_high_budget_movie_response_data(rating: str, genre: str, quan: str) -> Union[str, Dict[str, Any]]:
    """
    Функция отправляет запрос на сервер для поиска фильмов по бюджету.

    :param rating: Тип сортировки('1' для низкого бюджета, '-1' для высокого).
    :param genre: Жанр фильма.
    :param quan: Количество выводимых вариантов.
    :return: Словарь с данными о фильмах в случае успешного запроса или строку с сообщением об ошибке.
    """
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    }
    if rating == '1':
        sort_type = '1'
    else:
        sort_type = '-1'
    params = {"limit": quan,
              "selectFields": ['name', 'description', 'budget', 'ageRating', 'poster', 'type', 'year', 'rating',
                               'genres'],
              "notNullFields": ['name', 'description', 'year', 'rating.kp', 'ageRating', 'genres.name', 'poster.url'],
              'sortField': 'budget.value',
              "sortType": sort_type,
              'genres.name': genre
              }
    response = requests.get(URL, params=params, headers=headers)
    if response.status_code != 200:
        return 'Не удалось выполнить поиск'
    else:
        return json.loads(response.text)
