from db.get_data import list_db_data
from fuzzywuzzy import process, fuzz
import loader


def extract_keywords(sentence):
    '''Получение списка ключевых слов'''
    doc = loader.nlp(sentence)
    # Извлечение ключевых слов
    keywords = [
        token.text for token in doc if not token.is_stop and token.is_alpha]
    return keywords


def get_keyphrase(sentence):
    '''Преобразование фразы в строку с ключевыми словами'''
    keywords = extract_keywords(sentence)
    keyphrase = ' '.join(keywords)
    return keyphrase


def get_db_list_kewords():
    '''Преобразование списка вопросов в список ключевых слов'''
    for item in list_db_data:
        question = item.get('question')
        kw = extract_keywords(question)
        new_kp = ' '.join(kw)
        item['keyphrase'] = new_kp
        loader.db_list_keyphrases.append(item)


def sort_results(results, keyphrase):
    '''Сортировка списка результатов'''

    # сначала выбор тех, что выше порога
    above_the_threshold_results = [
        result for result in results if result[1] > loader.threshold_1]
    # потом сортировка по количеству совпавших слов
    compare_results_all = []
    for result in above_the_threshold_results:
        result_data = {
            'info': result,
            'compar_words_count': 0
        }
        db_keyphrase = result[0].split(' ')
        if isinstance(keyphrase, str):
            keyphrase = keyphrase.split(' ')
        # Сравниваем каждое слово из списка с каждым словом строки
        for token in db_keyphrase:
            for word in keyphrase:
                if fuzz.partial_ratio(token, word) >= loader.threshold_2:
                    result_data['compar_words_count'] += 1
                    break
        compare_results_all.append(result_data)
    sorted_results = sorted(
        compare_results_all, key=lambda x: x['compar_words_count'], reverse=True)
    return sorted_results


def get_answer_data(keyphrase):
    '''Получение данных для ответа'''

    db_list_keyphrases = [item.get('keyphrase')
                          for item in loader.db_list_keyphrases]
    compare_results_all = process.extractBests(keyphrase, db_list_keyphrases)
    results = sort_results(compare_results_all, keyphrase)

    if not results:
        print('Ничего не найдено')
        return None
    results = [result['info'] for result in results]
    return results
