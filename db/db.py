from peewee import Model, SqliteDatabase, TextField, BlobField, IntegerField

# Создаём соединение с базой данных
db = SqliteDatabase('db.sqlite')

# Определяем модель с использованием Peewee


class Question(Model):
    id = IntegerField(primary_key=True)
    question = TextField()
    vector = BlobField()
    answer = TextField()

    class Meta:
        database = db


# Создаём таблицы, если их ещё нет
db.connect()
# db.create_tables([Question])
