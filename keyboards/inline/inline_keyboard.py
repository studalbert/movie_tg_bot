from telebot import types

def get_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='movie_search')
    btn2 = types.InlineKeyboardButton(text='movie_by_rating')
    btn3 = types.InlineKeyboardButton(text='low_budget_movie')
    btn4 = types.InlineKeyboardButton(text='high_budget_movie')
    btn5 = types.InlineKeyboardButton(text='history')
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard

