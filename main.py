import api
import database
import handlers
import keyboards
import states
import utils
from telebot.custom_filters import StateFilter
from loader import bot

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()

