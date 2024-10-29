from telebot import types


def get_reply_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton('/help')
    keyboard.add(btn1)
    return keyboard
