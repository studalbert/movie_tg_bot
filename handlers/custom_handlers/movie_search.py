from api.movie_search_api import  movie_search_response_data
from loader import bot
from keyboards.reply.get_reply_keyboard import get_reply_keyboard
from states.movie_states import MovieState


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

        response_data = movie_search_response_data()
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