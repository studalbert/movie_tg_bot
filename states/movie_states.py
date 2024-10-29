from telebot.handler_backends import State, StatesGroup


class MovieState(StatesGroup):
    """Состояния для обработки фильмов."""

    movie_name = State()  # Ожидание ввода названия фильма
    quantity = State()  # Ожидание ввода количества выводимых вариантов
    nones = State()  # Состояние для завершения обработки


class RatingState(StatesGroup):
    """Состояния для обработки фильмов по рейтингу."""

    movie_rating = State()  # Ожидание ввода рейтинга фильма
    genre = State()  # Ожидание ввода жанра фильма
    quantity = State()  # Ожидание ввода количества выводимых вариантов
    nones = State()  # Состояние для завершения обработки


class LowBudgetMovie(StatesGroup):
    """Состояния для обработки фильмов с низким бюджетом."""

    genre = State()  # Ожидание ввода жанра фильма
    quantity = State()  # Ожидание ввода количества выводимых вариантов
    nones = State()  # Состояние для завершения обработки


class HighBudgetMovie(StatesGroup):
    """Состояния для обработки фильмов с высоким бюджетом."""

    genre = State()  # Ожидание ввода жанра фильма
    quantity = State()  # Ожидание ввода количества выводимых вариантов
    nones = State()  # Состояние для завершения обработки


class HistoryDate(StatesGroup):
    """Состояние для выбора даты истории запросов."""

    date = State()  # Ожидание ввода даты запроса
