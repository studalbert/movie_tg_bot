from telebot.handler_backends import State, StatesGroup

class MovieState(StatesGroup):
    movie_name = State()
    quantity = State()
    nones = State()

class RatingState(StatesGroup):
    movie_rating = State()
    genre = State()
    quantity = State()
    nones = State()

class LowBudgetMovie(StatesGroup):
    genre = State()
    quantity = State()
    nones = State()

class HighBudgetMovie(StatesGroup):
    genre = State()
    quantity = State()
    nones = State()
