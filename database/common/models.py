from peewee import *

db = SqliteDatabase('history.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField(primary_key=True, unique=True)

class History(BaseModel):
    user = ForeignKeyField(User, backref='movies')
    date = DateField()
    movie_name = CharField()
    description = CharField()
    rating = IntegerField()
    year = IntegerField()
    genre = CharField()
    age_rating = IntegerField()
    poster = CharField()
    def __str__(self):
        return (
                f'Дата поиска тайтла: {self.date}\n'
                f'Название: {self.movie_name}\n'
                f'Описание: {self.description}\n'
                f'Рейтинг: {self.rating}\n'
                f'Год производства: {self.year}\n'
                f'Жанр: {self.genre}\n'
                f'Возрастной рейтинг: {self.age_rating}\n'
        )

def create_models():
    db.create_tables([User, History])




