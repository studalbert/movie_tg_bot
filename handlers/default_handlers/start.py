from peewee import IntegrityError
from database.common.models import User
from loader import bot
from keyboards.reply.get_reply_keyboard import get_reply_keyboard


@bot.message_handler(commands=['start'])
def start(message):
    try:
        User.create(user_id = message.from_user.id)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
                                          f'Я бот, который поможет найти тебе твой любимый фильм или сериал.\n'
                                          f'Чтобы увидеть все мои функции и возможности, нажми на кнопку /help',
                         reply_markup=get_reply_keyboard())
    except IntegrityError:
        bot.send_message(message.chat.id, f'Рад вас снова видеть, {message.from_user.first_name} {message.from_user.last_name}\n'
                                      f'Я бот, который поможет найти тебе твой любимый фильм или сериал.\n'
                                      f'Чтобы увидеть все мои функции и возможности, нажми на кнопку /help',
                     reply_markup=get_reply_keyboard())