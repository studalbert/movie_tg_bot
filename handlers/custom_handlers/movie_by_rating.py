from telebot.types import Message
import re
from api.movie_by_rating_api import movie_by_rating_response_data
from loader import bot
from states.movie_states import RatingState
from utils.funcs import print_and_safe_info


@bot.message_handler(commands=['movie_by_rating'])
def movie_by_rating(message: Message) -> None:
    """
    Обработчик команды /movie_by_rating.

    Устанавливает состояние для ожидания ввода рейтинга или диапазона рейтинга фильмов.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    bot.set_state(message.from_user.id, RatingState.movie_rating, message.chat.id)
    bot.send_message(message.chat.id, 'Пожалуйста, введи рейтинг или диапазон рейтинга фильмов.(пример: 7, 10, 7.2-10)')


@bot.message_handler(state=RatingState.movie_rating)
def handle_movie_rating(message: Message) -> None:
    """
    Обработчик состояния ожидания ввода рейтинга фильма.

    Проверяет корректность введенного рейтинга или диапазона.
    Если ввод корректен, переходит к ожиданию ввода жанра фильма.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    if re.fullmatch(r'^(?:(?:[0-9]|10)(?:\.\d+)?|(?:[0-9](?:\.\d+)?)-(?:[0-9]|10)(?:\.\d+)?)$', message.text):
        bot.set_state(message.from_user.id, RatingState.genre, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['movie_rating'] = message.text
        bot.send_message(message.from_user.id, 'Отлично! Теперь введи жанр фильма.')
    else:
        bot.send_message(message.from_user.id,
                         "Неправильный ввод.Введи рейтинг или диапазон рейтинга фильмов.(пример: 7, 10, 7.2-10) ")


@bot.message_handler(state=RatingState.genre)
def handle_genre(message: Message) -> None:
    """
    Обработчик состояния ожидания ввода жанра фильма.

    Сохраняет введенный жанр в данные пользователя и запрашивает количество выводимых вариантов.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    bot.set_state(message.from_user.id, RatingState.quantity, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text
    bot.send_message(message.from_user.id, 'Отлично! Теперь введи количество выводимых вариантов.')


@bot.message_handler(state=RatingState.quantity)
def handle_rating_quantity(message: Message) -> None:
    """
    Обработчик состояния ожидания ввода количества выводимых вариантов.

    Проверяет, является ли введенное значение числом. Если да,
    сохраняет количество и вызывает функцию для получения данных о фильмах.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, RatingState.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        response_data = movie_by_rating_response_data(data['movie_rating'], data['genre'], data['quantity'])
        print_and_safe_info(bot, message, data['quantity'], response_data)
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")
