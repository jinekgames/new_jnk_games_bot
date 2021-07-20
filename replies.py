import random
import time
from time import daylight
random.seed(version=2)
import requests
session = requests.Session()
import vk_api
from vk_api.utils import get_random_id

import datetime

from scedullar import mmm19_scedullar


# for поздравить данила timeout
class MyClass:
    danil_bd_timer = 0


# check if txt does contain str
def _contain5(txt, str):

    iter_txt = 0
    iter_txt_new = 0
    iter_str = 0

    len_txt = len(txt)
    len_str = len(str)

    for iter_txt in range(len_txt):

        iter_txt_new = iter_txt
        iter_str = 0

        while iter_txt_new < len_txt and iter_str < len_str and txt[iter_txt_new] == str[iter_str]:
            iter_txt_new += 1
            iter_str += 1

        if iter_str == len_str:
            return True

    return False

# check if txt contains any of list strs
def contain5(txt, list):
    for str in list:
        if _contain5(txt, str):
            return True
    return False

# check if txt end woth str
def end5(txt, str):

    iter_str = len(str) - 1
    iter_txt = len(txt) - 1

    while iter_str >= 0 and iter_txt >=0:
        if txt[iter_txt] != str[iter_str]:
            return False
        iter_str -= 1
        iter_txt -= 1
    
    return True

# check if txt is str
def _i5(txt, str):
    
    iter_str = 0
    len_str = len(str)

    for ch in txt:
        if ch != str[iter_str]:
            return False
        iter_str += 1
        if iter_str == len_str:
            return True

    if iter_str != len_str:
        return False
    
    return True

# check if txt is any of list strs    
def i5(txt, list):
    for str in list:
        if _i5(txt, str):
            return True
    return False

# choose answer from the list
def choo5e(list):
    return list[random.randint( 0, len(list)-1 )]
            


# returns answer accornding to message
def msgProc(id, msg, vksession, myapi, upload, name):


    if msg != '':

        # BASE ANSWERS

        if contain5(msg, ['как меня зовут']):
            return name[0] + ' ' + name[1]

        if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам' ]):
            return choo5e([ 'привет', 'здарова заебал', 'как сам чел', 'Здравия желаю', 'Здравствуй, ' + name[0] ])

        elif end5(msg, 'да'):
            return choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова' ])
        elif end5(msg, 'нет'):
            return choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])
        elif contain5(msg, [ 'хах', 'хпх', 'хкх', 'hah', 'hhh', 'jaj', '[f[', 'хех', 'хых', 'а0а', 'фчф' ]) or i5(msg, [ 'ор', 'ржака', 'ржу', 'ржомба' ]):
            return choo5e([
                'РЖОМБА', 'Ебать я ору тоже', 'АХАХАХАХАХ))', 'Невероятная ржака', 'ахах)0', 'литчно я уже под столом',
                ')))))00))))))))))0))))))0))00000000)))))))))))))))))))))))0)0)0))0)0)0)))))',
                'лолирую', 'ржу уже третий день', 'Ржакаем всем сервером))0'
            ])

        elif end5(msg, 'ладно'):
            return 'прохладно'
        elif end5(msg, 'хуядно'):
            return 'прохладно'
        elif end5(msg, 'шоколадно'):
            return 'мармеладно'
        elif end5(msg, 'мармеладно'):
            return 'лимонадно'
        elif end5(msg, 'лимонадно'):
            return 'ладно'

        elif contain5(msg, [ 'пидор' ]):
            return choo5e([ 'сам пидор', 'пошел нахуй', 'gjitk yf[eq', 'sosi', 'ты че сука', 'а по ебалу??' ])
        elif contain5(msg, [ 'иди', 'пошел', 'пашел', 'пашол' ]) and contain5(msg, [ 'хуй', 'пизду' ]):
            return choo5e([ 'сам иди', 'пошел нахуй', 'gjitk yf[eq', 'sosi', 'ты че сука', 'а может ты?' ])
        elif msg.find('соси') != -1 :
            return choo5e([ 'сам соси сука', 'иди нахуй пидорас', 'чекай мать' ])
        elif msg.find('мать') != -1 :
            return choo5e([ 'серьезно чел, шутки про мать в ' + str( datetime.date.today().year ) ])
        elif msg.find('жир') != -1 :
            return choo5e([ 'не жир, а силовая броня' ])
        elif msg.find('резня') != -1 :
            return 'РЕЗНЯЯЯЯЯЯЯЯЯ'
        elif msg.find('гном') != -1 :
            return 'гном тут только ты'    



        # SHARAGA
            
        elif i5(msg, [ 'пн', 'понедельник' ]):
            return mmm19_scedullar[0]
        elif i5(msg, [ 'вт', 'вторник' ]):
            return mmm19_scedullar[1]
        elif i5(msg, [ 'ср', 'среда' ]):
            return mmm19_scedullar[2]
        elif i5(msg, [ 'чт', 'четверг' ]):
            return mmm19_scedullar[3]
        elif i5(msg, [ 'пт', 'пятница' ]):
            return mmm19_scedullar[4]
        elif i5(msg, [ 'сб', 'суббота' ]):
            return mmm19_scedullar[5]
        elif i5(msg, [ 'вс', 'воскресенье' ]):
            return mmm19_scedullar[6]

        elif i5(msg, [ 'сегодня' ]):
            return mmm19_scedullar[datetime.datetime.today().weekday()]
        elif i5(msg, [ 'завтра' ]):
            today = datetime.date.today()
            tomorrow = datetime.date(today.year, today.month, today.day+1)
            return mmm19_scedullar[tomorrow.weekday()]



        # HUINYA

        elif i5(msg, ['поздравить данила']):
            cur_time = time.time()
            if (cur_time - MyClass.danil_bd_timer > 120):
                MyClass.danil_bd_timer = cur_time
                myapi.wall.post(
                    owner_id = '-205950303',       # my id 190344587 community 205950303
                    from_group = 1,
                    message = 'ебать Данил с др нахуй\nОт: ' + name[0])
                return 'готово ебать'
            else:
                return 'братан, слишком часто'

        elif msg.startswith('поиск'):

            response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': msg[5:len(msg)],
                    'format': 'json'
                }
            ).json()

            #print(response)

            text = response.get('AbstractText')
            image_url = response.get('Image')
            wiki = response.get('AbstractURL')
            attachments = []

            if image_url or text:
                image = session.get('https://duckduckgo.com/' + image_url, stream=True)
                photo = upload.photo_messages(photos=image.raw)[0]

                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )

                print(text)

                vksession.method('messages.send',
                    {
                        'user_id': id,
                        'message': text,
                        'random_id': get_random_id(),
                        'attachment': ','.join(attachments)
                    })

                return 'не благодари'

            elif wiki:
                return response.get('AbstractURL')

            else:
                return 'нихуя не нашлось'



        # STUPID DIALOGS

        elif _contain5(msg, 'кто спрашивает'):
            return 'ну я спрашиваю'
        elif _contain5(msg, 'я спрашиваю'):
            return 'кто я?'
        elif _contain5(msg, 'кто я'):
            return 'смотря кто спрашивает'
