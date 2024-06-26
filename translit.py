import json
from razdel import tokenize
from pymorphy2 import MorphAnalyzer
import pandas as pd
from pymystem3 import Mystem

morph = MorphAnalyzer()
mystem = Mystem()

words = [
'нот', 'нат', 'ван', 'уан', 'ту', 'фри', 'телл', 'сэй', 'сэд', 'хэппи', 'лоуки', 'лайк', 'алледжедли', 'бести', 'инсейн', 'инсэйн', 'втф', 'фр', 'кайнда', 'спидран', 'герл', 'бой', 'гёрл', 'айм', 'твиннинг', 'зис', 'зыс', 'кэн', 'лукс', 'дэмн', 'дрим', 'хелп', 'хиз' 'соу', 'ай', 'си', 'хау', 'ит', 'кэнт', 'кен', 'кент', 'зе', 'крейзи', 'стрейт', 'тейк', 'иф', 'зет', 'хелпс', 'ду', 'гуд', 'фор', 'кьют', 'смолл', 'джаст', 'крэйзи', 'хи', 'ши', 'зэ', 'зей', 'энивэй', 'олрайт', 'хау', 'ду', 'слэй', 'хайки', 'стрэйт', 'белив', 'билив', 'ер', 'юр', 'ёр', 'юв', 'айв', 'гат', 'беттер', 'эвриван', 'эврибади', 'тейк', 'тред', 'краин', 'крайин', 'синг', 'дэнс', 'дэнсинг', 'шиз', 'хёр', 'сорри', 'ху', 'энивей', 'гейм', 'майнд', 'олсо', 'дюд', 'импоссибл', 'харт', 'вилл', 'райт', 'вэр', 'гесс', 'донт', 'вонт', 'поинт', 'вонна', 'фром', 'найс', 'велл', 'кул', 'шор', 'стилл', 'пипл', 'вайлд', 'тру', 'самфинг', 'сейм', 'энд', 'ресерч', 'крафчу', 'крафтить', 'генерю', 'нагенерю', 'трейнить', 'аттеншн', 'вайб', 'иннер', 'фикс', 'майт', 'финк' ]

excluded_words = ['1','2','3','4','5','6','7','8','9','0','папа','мама']

def read_json_and_get_dict(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    messages = []
    for element in data['messages']:
        if element['type'] == 'message':
            mess = element['text']
            if isinstance(mess, list):
                text = ''
                for el in mess:
                    if isinstance(el, dict):
                        text+=el['text']
            else:
                text = mess
            text_tokens = list(tokenize(text))
            if any((token.text in words) for token in text_tokens) and all((token.text not in excluded_words) for token in text_tokens):
            # if any((word in text) for word in words):
                record = {'text': text, 
                        'tokens': [{'token': token.text, 
                                    'method': str(morph.parse(token.text)[0].methods_stack[0][0]), 
                                    'pos': morph.parse(token.text)[0].tag.POS} for token in text_tokens]}
                messages.append(record)
    return messages

def get_translit_and_pos(message):
    translit=''
    pos_bef = [None, None, None]
    pos_aft = [None, None, None]
    # prev_token_meth
    i_left = 30
    i_right = 0
    for i, token in enumerate(message['tokens']):
        if (token['method'] in ['FakeDictionary()', 'UnknAnalyzer()']) or token['token'] in words:
            if i>=0 and i<i_left:
                i_left = i
            if i<=len(message['tokens']) and i>i_right:
                i_right = i
    if i_left!=i_right:
        translit = ' '.join([token['token'] for token in message['tokens'][i_left:i_right+1]])
    else:
        translit = message['tokens'][i_left]['token']
    if i_left > 0:
        pos_bef[0] = message['tokens'][i_left - 1]['pos']
    if i_left > 1:
        pos_bef[1] = message['tokens'][i_left - 2]['pos']
    if i_left>2:
        pos_bef[2] = message['tokens'][i_left - 3]['pos']
    if i_right < len(message['tokens']) - 1:
        pos_aft[0] = message['tokens'][i_right + 1]['pos']
    if i_right < len(message['tokens']) - 2:
        pos_aft[1] = message['tokens'][i_right + 2]['pos']
    if i_right < len(message['tokens']) - 3:
        pos_aft[2] = message['tokens'][i_right + 3]['pos']
    return translit, pos_bef, pos_aft

def make_df(messages):
    df = pd.DataFrame()
    texts = []
    translits = []
    pos_bef1 = []
    pos_bef2 = []
    pos_bef3 = []
    pos_aft1 = []
    pos_aft2 = []
    pos_aft3 = []
    for message in messages:
        texts.append(message['text'])
        translit, pos_bef, pos_aft = get_translit_and_pos(message)
        translits.append(translit)
        pos_bef1.append(pos_bef[0])
        pos_bef2.append(pos_bef[1])
        pos_bef3.append(pos_bef[2])
        pos_aft1.append(pos_aft[0])
        pos_aft2.append(pos_aft[1])
        pos_aft3.append(pos_aft[2])
    df['text'] = texts
    df['translit'] = translits
    df['pos_bef1'] = pos_bef1
    df['pos_bef2'] = pos_bef2
    df['pos_bef3'] = pos_bef3
    df['pos_aft1'] = pos_aft1
    df['pos_aft2'] = pos_aft2
    df['pos_aft3'] = pos_aft3
    return df

messages = read_json_and_get_dict(r'result.json')

df = make_df(messages)

df.to_csv('translit_dataset.csv', encoding='utf-16')
