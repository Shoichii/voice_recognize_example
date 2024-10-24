from sentence_transformers import SentenceTransformer

from db import Question
from get_data import data

# Загружаем модель Sentence-BERT
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def add_questions_to_db(questions_with_answers):
    """
    Функция принимает список словарей с полями вопрос и ответ,
    векторизует вопрос и сохраняет все данные в базу данных.

    Пример входных данных:
    questions_with_answers = [
        {"question": "Когда я смогу уйти в свой первый отпуск?", "answer": "Через год"},
        {"question": "Что входит в состав Бургер 'Сочная цыпа'?", "answer": "Курица, салат, булочка"},
    ]
    """
    for entry in questions_with_answers:
        # Векторизация вопроса
        vector = model.encode(entry['question'])

        # Преобразуем вектор в байтовый формат
        vector_bytes = vector.tobytes()

        # Сохраняем вопрос, вектор и ответ в базу данных
        Question.create(question=entry['question'],
                        vector=vector_bytes, answer=entry['answer'])


add_questions_to_db(data)
