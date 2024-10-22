import re
from api.movie_by_rating_api import movie_by_rating_response_data
from loader import bot
from keyboards.reply.get_reply_keyboard import get_reply_keyboard
from states.movie_states import RatingState


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
        response_data = movie_by_rating_response_data()
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