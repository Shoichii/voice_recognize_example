from db.get_data import data
from fuzzywuzzy import process, fuzz
import spacy

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")


def extract_keywords(sentence):
    doc = nlp(sentence)
    # Извлечение ключевых слов
    keywords = [
        token.text for token in doc if not token.is_stop and token.is_alpha]
    return keywords


# одиночный

def get_keyphrase(text):
    sentence = text
    keywords = extract_keywords(sentence)
    print("Ключевые слова:", keywords)
    keyphrase = ' '.join(keywords)
    return keyphrase
# keyphrase = sentence

# db_keywords = extract_keywords('когда я получу первую зарплату?')
# print(f'Ключевые слова из бд: {db_keywords}')
# db_keyphrase = ' '.join(db_keywords)
# b = fuzz.WRatio(db_keyphrase,
#                 keyphrase)

# print('===========')
# print('b : ' + str(b))


# список
def get_result(keyphrase):
    # keyphrase = 'сколько хранится нарезка голландского сыра дорог чикен'
    db_list_keyphrases = []
    for item in data:
        question = item.get('question')
        # db_list_keyphrases.append(question)
        kw = extract_keywords(question)
        new_kp = ' '.join(kw)
        db_list_keyphrases.append(new_kp)
    # db_list_keyphrases[8] += ' м4'
    # db_list_keyphrases[9] += ' м4'
    a = process.extractBests(keyphrase, db_list_keyphrases)
    print('===========')
    print('a : ' + str(a))
    print('===========')

    results = []
    number = 0
    for i, c in enumerate(a):
        if c[1] > 60:
            results.append(c)
    # if len(results) == 1:
    #     print(results[0])
    if not results:
        print('не найдено ничего')
    else:
        #     pass
        #     print('найдено несколько вариантов : ')
        #     for c in results:
        #         print(c)

        # перебор всех правильных ответов
        # и выбор самого подходящего
        final_results = []
        print('results', results)
        print('!!!!!!!!!!!!!!!!!')
        for res in results:
            obj = {
                'res': res,
                'count': 0
            }
            input_tokens = res[0].split(' ')
            print('keyphrase', keyphrase)
            print('тип keyphrase', type(keyphrase))
            print(isinstance(keyphrase, str))
            if isinstance(keyphrase, str):
                keyphrase = keyphrase.split(' ')
            for token in input_tokens:
                print('token', token)
                for word in keyphrase:
                    # Сравниваем каждое слово из списка с каждым токеном строки
                    print('word', word)
                    print('Есть ли совпадение', fuzz.partial_ratio(token, word))
                    if fuzz.partial_ratio(token, word) >= 80:
                        obj['count'] += 1
                        break
            final_results.append(obj)
            print(obj)
        print('!!!!!!!!!!!!!!!!!')
        print(final_results)
        final_final_results = sorted(
            final_results, key=lambda x: x['count'], reverse=True)
        print('================')
        print('================')
        print('Реально последний результат', final_final_results)
        print('Самое вероятное совпадение', final_final_results[0])


# какой состав цитрусовой заправки

# после определения результатов больше 60 брать все, что попались и сравнивать слова
# того, что спросил клиент и того, что нашлось
