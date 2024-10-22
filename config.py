import json
import re
from ast import Index
import telebot
from telebot import types
from dotenv import load_dotenv
import os
import requests
from telebot.handler_backends import State, StatesGroup
from telebot.types import ReplyKeyboardRemove
from telebot.custom_filters import StateFilter
from keyboards.inline.inline_keyboard import get_inline_keyboard
from keyboards.reply.get_reply_keyboard import get_reply_keyboard

load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
                                      f'Я бот, который поможет найти тебе твой любимый фильм или сериал.\n'
                                      f'Чтобы увидеть все мои функции и возможности, нажми на кнопку /help',
                     reply_markup=get_reply_keyboard())



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Доступные команды бота:\n'
                                      '/movie_search -  поиск фильма/сериала по названию;\n'
                                      '/movie_by_rating - поиск фильмов/сериалов по рейтингу;\n'
                                      '/low_budget_movie -  поиск фильмов/сериалов с низким бюджетом;\n'
                                      '/high_budget_movie - поиск фильмов/сериалов с высоким бюджетом;\n'
                                      '/history - возможность просмотра истории запросов и поиска фильма/сериала.',
                     reply_markup=ReplyKeyboardRemove())

class MovieState(StatesGroup):
    movie_name = State()
    quantity = State()
    nones = State()

@bot.message_handler(commands=['movie_search'])
def movie_search(message):
    bot.set_state(message.from_user.id, MovieState.movie_name, message.chat.id)
    bot.send_message(message.chat.id, 'Пожалуйста, введи название фильма или сериала.')

@bot.message_handler(state = MovieState.movie_name)
def handle_movie_name(message):
    bot.set_state(message.from_user.id, MovieState.quantity, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['movie_name'] = message.text
    bot.send_message(message.from_user.id, 'Отлично! Теперь введи количество выводимых вариантов.')

@bot.message_handler(state = MovieState.quantity)
def handle_quantity(message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, MovieState.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit={data['quantity']}&query={data['movie_name']}"
        headers = {
            "accept": "application/json",
            "X-API-KEY": API_KEY
        }
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        try:
            for i in range(int(data['quantity'])):
                bot.send_photo(message.chat.id, response_data['docs'][i]['poster']['url'])
                bot.send_message(message.from_user.id, f'Название: {response_data['docs'][i]['name']}\n'
                                                       f'Описание: {response_data['docs'][i]['description']}\n'
                                                       f'Рейтинг по кинопоиску: {response_data['docs'][i]['rating']['kp']}\n'
                                                       f'Год производства: {response_data['docs'][i]['year']}\n'
                                                       f'Жанр: {[elem['name'] for elem in response_data['docs'][i]['genres']]}\n'
                                                       f'Возрастной рейтинг: {response_data['docs'][i]['ageRating']}')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help', reply_markup=get_reply_keyboard())
            return
        except IndexError:
            bot.send_message(message.chat.id, 'Это все тайтлы, что я нашел:(')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                             reply_markup=get_reply_keyboard())
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")



class RatingState(StatesGroup):
    movie_rating = State()
    genre = State()
    quantity = State()
    nones = State()

@bot.message_handler(commands=['movie_by_rating'])
def movie_by_rating(message):
    bot.set_state(message.from_user.id, RatingState.movie_rating, message.chat.id)
    bot.send_message(message.chat.id, 'Пожалуйста, введи рейтинг или диапазон рейтинга фильмов.(пример: 7, 10, 7.2-10)')

@bot.message_handler(state = RatingState.movie_rating)
def handle_movie_rating(message):
    if re.fullmatch(r'^(?:(?:[0-9]|10)(?:\.\d+)?|(?:[0-9](?:\.\d+)?)-(?:[0-9]|10)(?:\.\d+)?)$', message.text):
        bot.set_state(message.from_user.id, RatingState.genre, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['movie_rating'] = message.text
        bot.send_message(message.from_user.id, 'Отлично! Теперь введи жанр фильма.')
    else:
        bot.send_message(message.from_user.id, "Неправильный ввод.Введи рейтинг или диапазон рейтинга фильмов.(пример: 7, 10, 7.2-10) ")

@bot.message_handler(state = RatingState.genre)
def handle_genre(message):
    bot.set_state(message.from_user.id, RatingState.quantity, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text
    bot.send_message(message.from_user.id, 'Отлично! Теперь введи количество выводимых вариантов.')

@bot.message_handler(state = RatingState.quantity)
def handle_rating_quantity(message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, RatingState.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit={data['quantity']}&selectFields=name&selectFields=description&selectFields=year&selectFields=ageRating&selectFields=genres&selectFields=rating&selectFields=poster&selectFields=budget&notNullFields=name&notNullFields=description&notNullFields=rating.kp&notNullFields=poster.url&notNullFields=ageRating&notNullFields=budget.value&sortField=rating.kp&sortType=1&rating.kp={data['movie_rating']}&genres.name={data['genre']}"

        headers = {
            "accept": "application/json",
            "X-API-KEY": API_KEY
        }
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        try:
            for i in range(int(data['quantity'])):
                bot.send_photo(message.chat.id, response_data['docs'][i]['poster']['url'])
                bot.send_message(message.from_user.id, f'Название: {response_data['docs'][i]['name']}\n'
                                                       f'Описание: {response_data['docs'][i]['description']}\n'
                                                       f'Рейтинг по кинопоиску: {response_data['docs'][i]['rating']['kp']}\n'
                                                       f'Год производства: {response_data['docs'][i]['year']}\n'
                                                       f'Жанр: {[elem['name'] for elem in response_data['docs'][i]['genres']]}\n'
                                                       f'Возрастной рейтинг: {response_data['docs'][i]['ageRating']}')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help', reply_markup=get_reply_keyboard())
            return
        except IndexError:
            bot.send_message(message.chat.id, 'Это все тайтлы, что я нашел:(')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                             reply_markup=get_reply_keyboard())
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")

class LowBudgetMovie(StatesGroup):
    genre = State()
    quantity = State()
    nones = State()

@bot.message_handler(commands=['low_budget_movie'])
def handle_genre(message):
    bot.set_state(message.from_user.id, LowBudgetMovie.genre, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи жанр фильма')

@bot.message_handler(state=LowBudgetMovie.genre)
def low_budget_movie(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text
    bot.set_state(message.from_user.id, LowBudgetMovie.quantity, message.chat.id)
    bot.send_message(message.from_user.id, 'Отлично!Теперь Введи количество выводимых вариантов.')

@bot.message_handler(state=LowBudgetMovie.quantity)
def handle_quantity(message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, LowBudgetMovie.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit={data['quantity']}&selectFields=name&selectFields=description&selectFields=budget&selectFields=rating&selectFields=ageRating&selectFields=genres&selectFields=poster&selectFields=year&notNullFields=name&notNullFields=description&notNullFields=year&notNullFields=ageRating&notNullFields=budget.value&sortField=budget.value&sortType=1&genres.name={data['genre']}"
        headers = {
            "accept": "application/json",
            "X-API-KEY": API_KEY
        }
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        try:
            for i in range(int(data['quantity'])):
                bot.send_photo(message.chat.id, response_data['docs'][i]['poster']['url'])
                bot.send_message(message.from_user.id, f'Название: {response_data['docs'][i]['name']}\n'
                                                       f'Описание: {response_data['docs'][i]['description']}\n'
                                                       f'Рейтинг по кинопоиску: {response_data['docs'][i]['rating']['kp']}\n'
                                                       f'Год производства: {response_data['docs'][i]['year']}\n'
                                                       f'Жанр: {[elem['name'] for elem in response_data['docs'][i]['genres']]}\n'
                                                       f'Возрастной рейтинг: {response_data['docs'][i]['ageRating']}\n'
                                                       f'Бюджет: {response_data['docs'][i]['budget']['value']} {response_data['docs'][i]['budget']['currency']}')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help', reply_markup=get_reply_keyboard())
            return
        except IndexError:
            bot.send_message(message.chat.id, 'Это все тайтлы, что я нашел:(')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                             reply_markup=get_reply_keyboard())
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")

class HighBudgetMovie(StatesGroup):
    genre = State()
    quantity = State()
    nones = State()

@bot.message_handler(commands=['high_budget_movie'])
def handle_genre(message):
    bot.set_state(message.from_user.id, HighBudgetMovie.genre, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи жанр фильма')

@bot.message_handler(state=HighBudgetMovie.genre)
def low_budget_movie(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text
    bot.set_state(message.from_user.id, HighBudgetMovie.quantity, message.chat.id)
    bot.send_message(message.from_user.id, 'Отлично!Теперь Введи количество выводимых вариантов.')

@bot.message_handler(state=HighBudgetMovie.quantity)
def handle_quantity(message):
    if message.text.isdigit():
        bot.set_state(message.from_user.id, HighBudgetMovie.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit={data['quantity']}&selectFields=name&selectFields=description&selectFields=budget&selectFields=rating&selectFields=ageRating&selectFields=genres&selectFields=poster&selectFields=year&notNullFields=name&notNullFields=description&notNullFields=year&notNullFields=ageRating&notNullFields=budget.value&sortField=budget.value&sortType=-1&genres.name={data['genre']}"
        headers = {
            "accept": "application/json",
            "X-API-KEY": API_KEY
        }
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        try:
            for i in range(int(data['quantity'])):
                bot.send_photo(message.chat.id, response_data['docs'][i]['poster']['url'])
                bot.send_message(message.from_user.id, f'Название: {response_data['docs'][i]['name']}\n'
                                                       f'Описание: {response_data['docs'][i]['description']}\n'
                                                       f'Рейтинг по кинопоиску: {response_data['docs'][i]['rating']['kp']}\n'
                                                       f'Год производства: {response_data['docs'][i]['year']}\n'
                                                       f'Жанр: {[elem['name'] for elem in response_data['docs'][i]['genres']]}\n'
                                                       f'Возрастной рейтинг: {response_data['docs'][i]['ageRating']}\n'
                                 f'Бюджет: {response_data['docs'][i]['budget']['value']} {response_data['docs'][i]['budget']['currency']}')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help', reply_markup=get_reply_keyboard())
            return
        except IndexError:
            bot.send_message(message.chat.id, 'Это все тайтлы, что я нашел:(')
            bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                             reply_markup=get_reply_keyboard())
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")


bot.add_custom_filter(StateFilter(bot))
bot.infinity_polling()