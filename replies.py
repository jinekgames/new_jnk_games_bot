import random
import time
random.seed(version=2)
import requests
session = requests.Session()
import json
import vk_api
from vk_api.utils import get_random_id

import datetime
import calendar

import users_db

from scedullar import weekday_ru_en


# some static variables
class SomeVars:
    timers = {}
    timeout = 60


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
    if (not id in SomeVars.timers) or (cur_time - SomeVars.timers[id] > SomeVars.timeout):
        SomeVars.timers[id] = cur_time
        rtrn_msg = ''
        try:
            vksession.method('messages.send',
                    {
                        'user_id': id,
                        'message': msg,
                        'random_id': get_random_id(),
                    })
            rtrn_msg = 'готово, с вас three hundred bucks'
        except vk_api.exceptions.ApiError:
            rtrn_msg = 'сначала заставь его чтото написать боту хоть раз, чтобы бот смог отправить ему сообщение'
        return rtrn_msg
    else:
        return 'этому челу уже писали за последние 2 минуты'




            


# returns answer accornding to message
def msgProc(id, msg, vksession, myapi, upload):


    if msg != '':



        # getting userdata from db
        userData = users_db.getUserData(id)
        if not userData:
            return 'возникла ошибка при поиске вашей записи в базе данных, пожалуйста, сообщите админу\n@eugene_programmist'




        # HUINYA

        if msg.startswith('makeadmin'):
            if not users_db.getUserData(id)['admin']:
                return 'назначать админов могут толкьо админы'

            id_ = msg.split(' ')
            if len(id_) != 2:
                return 'incorrect sintaxys'
            id_ = id_[1]
            userData_ = users_db.getUserData(id_)
            if not userData_:
                return 'user not found'
            userData_['admin'] = True
            users_db.add2List(id_, userData_)
            users_db.dumbList()
            return 'done'

        if msg.startswith('makenotadmin'):
            if not users_db.getUserData(id)['admin']:
                return 'убирать админов могут только админы'

            id_ = msg.split(' ')
            if len(id_) != 2:
                return 'incorrect sintaxys'
            id_ = id_[1]
            userData_ = users_db.getUserData(id_)
            if not userData_:
                return 'user not found'
            userData_['admin'] = False
            users_db.add2List(id_, userData_)
            users_db.dumbList()
            return 'done'


        if contain5(msg, [ 'поздравить', 'подравляю', 'поздравляю', 'с др' ]):

            if contain5(msg, [ 'данила', 'донила', 'даниила' ]):
                return sendMsg2id(vksession, 187191431, userData['name'][0] + ' поздравил тебя с др')

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
                if users_db.getUserData(id_):
                    if users_db.getUserData(id_)['admin']:
                        return 'сам пошел нахуй'
                return sendMsg2id(vksession, id_, 'ктото послал тебя нахуй')

        elif msg.startswith('написать'):
            if (msg.find('\n') == -1) or len(msg) < 18:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nнаписать 187191431\nвылези из под стола'
            msg_split = msg.split('\n')
            msg_split_command = msg_split[0].split(' ')
            id_ = msg_split_command[1]
            if len(msg_split_command) > 2 and msg_split_command[2] == 'анон':
                text = msg_split[1]
            else:
                text = userData['name'][0] + ' оставил тебе сообщение:\n' + msg_split[1]
            return sendMsg2id(vksession, id_, text)

        elif msg.startswith('отправить'):
            if (msg.find('\n') == -1) or len(msg) < 12:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nотправить jnk\nчел ты гений'
            msg_split = msg.split('\n')
            msg_split_command = msg_split[0].split(' ')
            id_ = users_db.findIdByName(msg_split_command[1])
            if not id_:
                return 'такого чела нет в моих с(письках)'
            if len(msg_split_command) > 2 and msg_split_command[2] == 'анон':
                text = msg_split[1]
            else:
                text = userData['name'][0] + ' оставил тебе сообщение:\n' + msg_split[1]
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

        

        # USER DATA FUNCTIONS

        elif msg.startswith('сменить ник'):
            new_nick = msg.split(' ')[2]
            userData['nick'] = new_nick
            users_db.add2List(id, userData)
            return 'изи'



        # SHARAGA
            
        elif msg == 'пн' or msg == 'понедельник':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Monday']
        elif msg == 'вт' or msg == 'вторник':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Tuesday']
        elif msg == 'ср' or msg == 'среда':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Wednesday']
        elif msg == 'чт'or msg == 'четверг':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Thursday']
        elif msg == 'пт' or msg == 'пятница':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Friday']
        elif msg == 'сб' or msg == 'суббота':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Saturday']
        elif msg == 'вс' or msg == 'воскресенье':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar['Sunday']

        elif msg == 'сегодня':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[calendar.day_name[datetime.datetime.today().weekday()]]
        elif msg == 'завтра':
            today = datetime.date.today()
            tomorrow = datetime.date(today.year, today.month, today.day+1)
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[calendar.day_name[tomorrow.weekday()]]

        elif msg == 'неделя':
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            text = ''
            for day in scedullar:
                text.join(scedullar[day] + '\n\n')
            return text


        elif msg.startswith('редактировать'):

            if not users_db.getUserData(id)['admin']:
                return 'менять расписание могут толкьо админы'

            try:

                commands = msg.split('\n')
                start_pointer = len(commands[0])
                if len(commands) < 2:
                    return 'неправильная команда'
                commands = commands[0].split(' ')
                if len(commands) < 2:
                    return 'неправильная команда'

                weekday = weekday_ru_en( commands[1] )
                if not weekday:
                    return 'неправильная команда'
                new_text = msg[ start_pointer+1 : len(msg) ]

                with open("scedullar.json", "r") as f:
                    scedullar = json.load(f)
                del scedullar[weekday]
                scedullar[weekday] = new_text
                scedullar_update_str = json.dumps(scedullar, sort_keys=True, indent=4)
                with open('scedullar.json', 'w') as f:
                    f.write(scedullar_update_str)

            except BaseException:

                return 'случилась ошибка скажи одмену пустб починит'

            return 'проверять будеш?'



        # BASE ANSWERS

        elif contain5(msg, ['как меня зовут']):
            return userData['name'][0] + ' ' + userData['name'][1]

        elif msg.startswith('кто ты'):
            return choo5e([ 'да', 'тебя это ебать не должно', 'я?', 'я бот ашо', 'не важно кто, важно кто' ])

        if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам', 'добрый ', 'здравствуй' ]):
            return choo5e([ 'здарова, отец', 'привет', 'здарова заебал', 'как сам чел', 'Здравия желаю', 'Здравствуй, ' + userData['name'][0] ])

        elif _end5(msg, 'да'):
            return choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова', 'правильно' ])
        elif _end5(msg, 'нет'):
            return choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])
        elif endswith_list(msg, [ '[ff', 'хаа', 'хах', 'хвх', 'аха', 'хпх', 'хкх', 'hah', 'hhh', 'jaj', '[f[', 'хех', 'хых', 'а0а', 'фчф', 'ору', 'ржака', 'ржу', 'ржомба' ]):
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



        # STUPID DIALOGS

        elif _contain5(msg, 'кто спрашивает'):
            return 'ну я спрашиваю'
        elif _contain5(msg, 'я спрашиваю'):
            return 'кто я?'
        elif _contain5(msg, 'кто я'):
            return 'смотря кто спрашивает'
