from telebot.types import Message
from api.low_high_budget_movie_api import low_high_budget_movie_response_data
from loader import bot
from states.movie_states import LowBudgetMovie
from utils.funcs import print_and_safe_info


@bot.message_handler(commands=['low_budget_movie'])
def handle_genre(message: Message) -> None:
    """
    Обработчик команды /low_budget_movie.

    Устанавливает состояние для ожидания ввода жанра фильма.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    bot.set_state(message.from_user.id, LowBudgetMovie.genre, message.chat.id)
    bot.send_message(message.from_user.id, 'Введи жанр фильма')


@bot.message_handler(state=LowBudgetMovie.genre)
def low_budget_movie(message: Message) -> None:
    """
    Обработчик состояния ожидания ввода жанра фильма.

    Сохраняет введенный жанр в данные пользователя и запрашивает количество выводимых вариантов.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    with bot.retrieve_data(message.from_user.id) as data:
        data['genre'] = message.text
    bot.set_state(message.from_user.id, LowBudgetMovie.quantity, message.chat.id)
    bot.send_message(message.from_user.id, 'Отлично!Теперь Введи количество выводимых вариантов.')


@bot.message_handler(state=LowBudgetMovie.quantity)
def handle_quantity(message: Message) -> None:
    """
    Обработчик состояния ожидания ввода количества выводимых вариантов.

    Проверяет, является ли введенное значение числом. Если да,
    сохраняет количество и вызывает функцию для получения данных о фильмах.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, LowBudgetMovie.nones, message.chat.id)
        with bot.retrieve_data(message.from_user.id) as data:
            data['quantity'] = message.text
        response_data = low_high_budget_movie_response_data('1', data['genre'], data['quantity'])
        print_and_safe_info(bot, message, data['quantity'], response_data)
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")
