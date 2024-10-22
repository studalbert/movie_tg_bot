from api.low_budget_movie_api import low_budget_movie_response_data
from loader import bot
from keyboards.reply.get_reply_keyboard import get_reply_keyboard
from states.movie_states import LowBudgetMovie


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
        response_data = low_budget_movie_response_data()
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