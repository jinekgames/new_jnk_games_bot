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


# some static variables
class SomeVars:
    timers = {}
    elite = {
        '190344587': True,
        '214156033': True
    }


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

# check if txt ends with str
def _end5(txt, str):

    iter_str = len(str) - 1
    iter_txt = len(txt) - 1

    while iter_str >= 0 and iter_txt >=0:
        if txt[iter_txt] != str[iter_str]:
            return False
        iter_str -= 1
        iter_txt -= 1
    
    return True

# check if txt ends with any of list strs    
def end5(txt, list):
    for str in list:
        if _end5(txt, str):
            return True
    return False

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

def endswith_list(msg, list):
    for str in list:
        if msg.endswith(str):
            return True
    return False


def sendMsg2id(vksession, id, msg):
    cur_time = time.time()
    if (not id in SomeVars.timers) or (cur_time - SomeVars.timers[id] > 120):
        SomeVars.timers[id] = cur_time
        rtrn_msg = ''
        try:
            print(vksession.method('messages.send',
                    {
                        'user_id': id,
                        'message': msg,
                        'random_id': get_random_id(),
                    }))
            rtrn_msg = 'готово, с вас three hundred bucks'
        except vk_api.exceptions.ApiError:
            rtrn_msg = 'сначала заставь его чтото написать боту хоть раз, чтобы бот смог отправить ему сообщение'
        return rtrn_msg
    else:
        return 'этому челу уже писали за последние 2 минуты'




            


# returns answer accornding to message
def msgProc(id, msg, vksession, myapi, upload, name):


    if msg != '':



    # HUINYA

        if contain5(msg, [ 'поздравить', 'подравляю', 'поздравляю', 'с др' ]):

            if contain5(msg, [ 'данила', 'донила', 'даниила' ]):
                return sendMsg2id(vksession, 187191431, name[0] + ' поздравил тебя с др')

                # это типа раньше он еще пост на стене дропал (чисток акпример тут пока будет)
                myapi.wall.post(
                    owner_id = '-205950303',       # my id 190344587 community 205950303
                    from_group = 1,
                    message = 'ебать Данил с др нахуй\nОт: ' + name[0])
            
            # elif contain5(msg, [ 'ртура', 'ртурчика', 'ртур4ика' ]):
            #     return sendMsg2id(vksession, 214156033, name[0] + ' поздравил тебя с др')

        elif msg.startswith('послать'):
            id_ = msg.split(' ')[1]
            if len(id_) != 9 or (not id_.isdigit()):
                return 'введите корректный айди чела которого надо послать'
            else:
                if id_ in SomeVars.elite:
                    return 'сам пошел нахуй'
                return sendMsg2id(vksession, id_, 'ктото послал тебя нахуй')

        elif msg.startswith('написать'):
            if (msg.find('\n') == -1) or len(msg) < 18:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nнаписать 187191431\nвылези из под стола'
            msg_split = msg.split('\n')
            msg_split_command = msg_split[0].split(' ')
            id_ = msg_split_command[1]
            if len(msg_split_command) == 3:
                if msg_split_command[2] == 'анон':
                    text = msg_split[1]
                else:
                    text = name[0] + ' оставил тебе сообщение:\n' + msg_split[1]
            else:
                text = name[0] + ' оставил тебе сообщение:\n' + msg_split[1]   
            return sendMsg2id(vksession, id_, text)

        


        elif msg.startswith('поиск'):

            response = session.get(
                'http://api.duckduckgo.com/',
                params={
                    'q': msg[5:len(msg)],
                    'format': 'json'
                }
            ).json()

            text = response.get('AbstractText')
            image_url = response.get('Image')
            wiki = response.get('AbstractURL')
            attachments = []

            if image_url:
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

            elif text:
                vksession.method('messages.send',
                    {
                        'user_id': id,
                        'message': text,
                        'random_id': get_random_id(),
                    })

                return 'не благодари'

            elif wiki:
                return response.get('AbstractURL')

            else:
                return 'нихуя не нашлось'




        # BASE ANSWERS

        elif contain5(msg, ['как меня зовут']):
            return name[0] + ' ' + name[1]

        elif msg.startswith('кто ты'):
            return choo5e([ 'да', 'тебя это ебать не должно', 'я?', 'я бот ашо', 'не важно кто, важно кто' ])

        if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам', 'добрый ', 'здравствуй' ]):
            return choo5e([ 'здарова, отец', 'привет', 'здарова заебал', 'как сам чел', 'Здравия желаю', 'Здравствуй, ' + name[0] ])

        elif _end5(msg, 'да'):
            return choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова', 'правильно' ])
        elif _end5(msg, 'нет'):
            return choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])
        elif endswith_list(msg, [ 'хах', 'хвх', 'аха', 'хпх', 'хкх', 'hah', 'hhh', 'jaj', '[f[', 'хех', 'хых', 'а0а', 'фчф', 'ору', 'ржака', 'ржу', 'ржомба' ]):
            return choo5e([
                'РЖОМБА', 'Ебать я ору тоже', 'АХАХАХАХАХ))', 'Невероятная ржака', 'ахах)0',
                ')))))00))))))))))0))))))0))00000000)))))))))))))))))))))))0)0)0))0)0)0)))))',
                'лолирую', 'ржу уже третий день', 'Ржакаем всем сервером))0'
            ])
        elif end5(msg, [ 'але', 'ало', 'алло' ]):
            return choo5e([ 'да', 'да-да', 'але да', 'че', 'ты куда звонишь' ])

        elif msg.startswith('правильно'):
            return 'спасибо брат'
        elif msg.startswith('спасибо' ):
            return choo5e([ 'обращайся, братик', 'пожалуйста', 'чел ;3' ])
        elif msg.startswith('зачем'):
            return choo5e([ 'затем', 'так надо' ])
        elif msg.startswith('почему'):
            return choo5e([ 'потому', 'по клавиатуре' ])
        elif msg.startswith('красиво'):
            return 'базаришь'

        elif _end5(msg, 'ладно'):
            return 'прохладно'
        elif _end5(msg, 'хуядно'):
            return 'прохладно'
        elif _end5(msg, 'шоколадно'):
            return 'мармеладно'
        elif _end5(msg, 'мармеладно'):
            return 'лимонадно'
        elif _end5(msg, 'лимонадно'):
            return 'ладно'

        elif msg.startswith('пидора ответ'):
            return choo5e([ 'шлюхи аргумент' ])
        elif contain5(msg, [ 'пидор' ]):
            return choo5e([ 'сам пидор', 'пошел нахуй', 'gjitk yf[eq', 'sosi', 'ты че сука', 'а по ебалу??' ])
        elif contain5(msg, [ 'иди', 'пошел', 'пашел', 'пашол', 'пашол', 'пошол', 'пошёл', 'gjitk' ]) and contain5(msg, [ 'хуй', 'пизду', '[eq' ]):
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
        elif contain5(msg, [ 'уебок', 'уебан', 'мудак', 'гнида', 'хуесос', 'мудила', 'ебан', 'конченый', 'долбаеб', 'лох' ]):
            return choo5e([ 'ой да иди в пизду долбаеб блять', 'ебало закрой', msg, 'хули ты обзываешься пидорас', 'говоришь на меня переводишь на себя нахуй' ])
        elif msg.find('ахуел') != -1 or msg.find('охуел') != -1:
            return choo5e([ 'сам охуел', 'а может ты охуел?', 'нет' ])
        elif msg.find('заебал') != -1:
            return choo5e([ 'сам заебал', 'это ты заебал' ])



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



        # STUPID DIALOGS

        elif _contain5(msg, 'кто спрашивает'):
            return 'ну я спрашиваю'
        elif _contain5(msg, 'я спрашиваю'):
            return 'кто я?'
        elif _contain5(msg, 'кто я'):
            return 'смотря кто спрашивает'
