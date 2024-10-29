from telebot.types import Message
from telebot.types import ReplyKeyboardRemove
from loader import bot


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    """
    Обработчик команды /help.

    Отправляет пользователю список доступных команд бота.

    :param message: Объект сообщения, содержащий информацию о пользователе и чате.
    """
    bot.send_message(message.chat.id, 'Доступные команды бота:\n'
                                      '/movie_search -  поиск фильма/сериала по названию;\n'
                                      '/movie_by_rating - поиск фильмов/сериалов по рейтингу;\n'
                                      '/low_budget_movie -  поиск фильмов/сериалов с низким бюджетом;\n'
                                      '/high_budget_movie - поиск фильмов/сериалов с высоким бюджетом;\n'
                                      '/history - возможность просмотра истории запросов и поиска фильма/сериала.',
                     reply_markup=ReplyKeyboardRemove())
