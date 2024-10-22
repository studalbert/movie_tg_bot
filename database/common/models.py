from peewee import *

db = SqliteDatabase('history.db')

class History(Model):
    user_id = IntegerField(primary_key=True)
    movie = CharField()
    date = DateField()
    class Meta:
        database = db

