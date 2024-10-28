from api.movie_search_api import movie_search_response_data
from loader import bot
from states.movie_states import MovieState
from utils.funcs import print_and_safe_info


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

        response_data = movie_search_response_data(data['quantity'], data['movie_name'])
        print_and_safe_info(bot, message, data['quantity'], response_data)
    else:
        bot.send_message(message.from_user.id, "Количество выводимых вариантов должно быть указано числом.")