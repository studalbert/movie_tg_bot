from datetime import datetime
from config import DATE_FORMAT
from database.common.models import History
from keyboards.reply.get_reply_keyboard import get_reply_keyboard

def print_and_safe_info(bot, message, count, response_data):
    due_date_string = datetime.now().strftime(DATE_FORMAT)
    try:
        for i in range(int(count)):
            bot.send_photo(message.chat.id, response_data['docs'][i]['poster']['url'])
            bot.send_message(message.from_user.id, f'Название: {response_data['docs'][i]['name']}\n'
                                                   f'Описание: {response_data['docs'][i]['description']}\n'
                                                   f'Рейтинг по кинопоиску: {response_data['docs'][i]['rating']['kp']}\n'
                                                   f'Год производства: {response_data['docs'][i]['year']}\n'
                                                   f'Жанр: {[elem['name'] for elem in response_data['docs'][i]['genres']]}\n'
                                                   f'Возрастной рейтинг: {response_data['docs'][i]['ageRating']}')
            new_hist = History(user=message.from_user.id,
                               date=due_date_string,
                               movie_name=response_data['docs'][i]['name'],
                               description=response_data['docs'][i]['description'],
                               rating=response_data['docs'][i]['rating']['kp'],
                               year=response_data['docs'][i]['year'],
                               genre=str([elem['name'] for elem in response_data['docs'][i]['genres']]),
                               age_rating=response_data['docs'][i]['ageRating'],
                               poster=response_data['docs'][i]['poster']['url'])
            new_hist.save()
        bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                         reply_markup=get_reply_keyboard())
        return

    except IndexError:
        bot.send_message(message.chat.id, 'Это все тайтлы, что я нашел:(')
        bot.send_message(message.chat.id, 'Чтобы вывести доступные команды нажмите на кнопку help',
                         reply_markup=get_reply_keyboard())