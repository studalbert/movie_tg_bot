from database.common.models import User, History
from keyboards.reply.get_reply_keyboard import get_reply_keyboard
from loader import bot
from states.movie_states import HistoryDate


@bot.message_handler(commands=['history'])
def history(message):
    bot.set_state(message.from_user.id, HistoryDate.date, message.chat.id)
    bot.send_message(message.from_user.id, 'Пожалуйста, введите за какую дату показать историю запросов (пример: 01.01.2001)')

@bot.message_handler(state=HistoryDate.date)
def handle_history(message):

    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    with bot.retrieve_data(message.from_user.id) as data:
        data['date'] = message.text
    movies = user.movies.where(History.date == data['date'])
    if not movies:
        bot.send_message(message.from_user.id, 'Нет запросов в эту дату.')
        bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                         reply_markup=get_reply_keyboard())
        bot.delete_state(message.from_user.id)
        return
    else:
        for movie in movies:
            bot.send_photo(message.from_user.id, movie.poster)
            bot.send_message(message.from_user.id, movie)
        bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                                               reply_markup=get_reply_keyboard())