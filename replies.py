from users_db import usersDataBase
import help_msgs
import random
import time
import requests
import json
import datetime
import calendar
from scedullar import weekday_ru_en
import vk_api
from vk_api.utils import get_random_id


random.seed(version=2)
requestSession = requests.Session()


# some static variables
class SomeVars:
    timers = {}
    timeoutSec = 60


# check if txt does contain str
def _contain5(text, str):

    iter_txt = 0
    iter_txt_new = 0
    iter_str = 0

    len_txt = len(text)
    len_str = len(str)

    for iter_txt in range(len_txt):

        iter_txt_new = iter_txt
        iter_str = 0

        while iter_txt_new < len_txt and iter_str < len_str and text[iter_txt_new] == str[iter_str]:
            iter_txt_new += 1
            iter_str += 1

        if iter_str == len_str:
            return True

    return False

# check if text contains any of list strs
def contain5(text, list):
    for str in list:
        if _contain5(text, str):
            return True
    return False

# check if text ends with str
def _end5(text, str):

    iter_str = len(str) - 1
    iter_txt = len(text) - 1

    while iter_str >= 0 and iter_txt >=0:
        if text[iter_txt] != str[iter_str]:
            return False
        iter_str -= 1
        iter_txt -= 1
    
    return True

# check if text ends with any of list strs    
def end5(text, list):
    for str in list:
        if _end5(text, str):
            return True
    return False

# check if text is str
def _i5(text, str):
    
    iter_str = 0
    len_str = len(str)

    for ch in text:
        if ch != str[iter_str]:
            return False
        iter_str += 1
        if iter_str == len_str:
            return True

    if iter_str != len_str:
        return False
    
    return True

# check if text is any of list strs    
def i5(text, list):
    for str in list:
        if _i5(text, str):
            return True
    return False

# choose answer from the list
def choo5e(list):
    return list[random.randint( 0, len(list)-1 )]

# check if text ends with any of list strs    
def endswith_list(text, list):
    for str in list:
        if text.endswith(str):
            return True
    return False

# send vk message to id
def sendMsg2id(vksession, id, msg):
    cur_time = time.time()
    if (not id in SomeVars.timers) or (cur_time - SomeVars.timers[id] > SomeVars.timeoutSec):
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


# return reply for user accornding to message
def msgProc(id, msg, vksession, myapi, upload):

    if msg != '':

        # get userdata from db
        userData = usersDataBase.getUserData(id)
        if not userData:
            return 'возникла ошибка при поиске вашей записи в базе данных, пожалуйста, сообщите админу\n@eugene_programmist'



        # HUINYA

        if msg.startswith('makeadmin'):
            if not usersDataBase.getUserData(id)['admin']:
                return 'назначать админов могут толкьо админы'

            distId = msg.split(' ')
            if len(distId) != 2:
                return 'incorrect sintaxys'
            distId = distId[1]
            userData_ = usersDataBase.getUserData(distId)
            if not userData_:
                return 'user not found'
            userData_['admin'] = True
            usersDataBase.add2List(distId, userData_)
            usersDataBase.dumbList()
            return 'done'

        elif msg.startswith('makenotadmin'):
            if not usersDataBase.getUserData(id)['admin']:
                return 'убирать админов могут только админы'

            distId = msg.split(' ')
            if len(distId) != 2:
                return 'incorrect sintaxys'
            distId = distId[1]
            userData_ = usersDataBase.getUserData(distId)
            if not userData_:
                return 'user not found'
            userData_['admin'] = False
            usersDataBase.add2List(distId, userData_)
            usersDataBase.dumbList()
            return 'done'


        elif contain5(msg, [ 'поздравить', 'подравляю', 'поздравляю', 'с др' ]):
            if contain5(msg, [ 'данила', 'донила', 'даниила' ]):
                return sendMsg2id(vksession, 187191431, userData['firstname'] + ' поздравил тебя с др')
                """
                # это типа раньше он еще пост на стене дропал (чисток акпример тут пока будет)
                myapi.wall.post(
                    owner_id = '-205950303',       # my id 190344587 community 205950303
                    from_group = 1,
                    message = 'ебать Данил с др нахуй\nОт: ' + userData['firstname'])
                """

        elif msg.startswith('послать'):
            distId = msg.split(' ')[1]
            if len(distId) != 9 or (not distId.isdigit()):
                return 'введите корректный айди чела которого надо послать'
            else:
                if usersDataBase.getUserData(distId):
                    if usersDataBase.getUserData(distId)['admin']:
                        return 'сам пошел нахуй'
                return sendMsg2id(vksession, distId, 'ктото послал тебя нахуй')

        elif msg.startswith('написать'):
            if (msg.find('\n') == -1) or len(msg) < 18:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nнаписать 187191431\nвылези из под стола'
            msg_split = msg.split('\n')
            msg_split_command = msg_split[0].split(' ')
            distId = msg_split_command[1]
            if len(msg_split_command) > 2 and msg_split_command[2] == 'анон':
                text = msg_split[1]
            else:
                text = userData['firstname'] + ' оставил тебе сообщение:\n' + msg_split[1]
            return sendMsg2id(vksession, distId, text)

        elif msg.startswith('отправить'):
            if (msg.find('\n') == -1) or len(msg) < 12:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nотправить jnk\nчел ты гений'
            msg_split = msg.split('\n')
            msg_split_command = msg_split[0].split(' ')
            distId = usersDataBase.findIdByField('firstname', msg_split_command[1])
            if not distId:
                distId = usersDataBase.findIdByField('nick', msg_split_command[1])
            if not distId:
                return 'такого чела нет в моих с(письках)'
            if len(msg_split_command) > 2 and msg_split_command[2] == 'анон':
                text = msg_split[1]
            else:
                text = userData['firstname'] + ' оставил тебе сообщение:\n' + msg_split[1]
            return sendMsg2id(vksession, distId, text)

        elif msg.startswith('поиск'):

            response = requestSession.get(
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
                image = requestSession.get('https://duckduckgo.com/' + image_url, stream=True)
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

        elif msg == 'help' or msg == 'команды':
            if userData['admin']:
                return help_msgs.admin_msg
            else:
                return help_msgs.nonadmin_msg

        

        # USER DATA FUNCTIONS

        elif msg.startswith('сменить ник'):
            new_nick = msg.split(' ')[2]
            userData['nick'] = new_nick
            usersDataBase.add2List(id, userData)
            return 'изи'



        # SHARAGA

        elif msg.startswith('группа'):
            group = msg.split(' ')
            if len(group) != 2:
                print(group)
                return 'неправильная команда\nправилльно так:\nгруппа 381904'
            group = group[1]
            if not group.isdigit():
                return 'нужно написать номер группы (только цифры (тире тоже не надо, хотя откуда у тебя тире, ты шо, не из ммм, ты как меня нашел))'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            if not group in scedullar:
                return 'такой группы еще нет в боте, попроси @eugene_programmist добавить твою группу'
            userData['group'] = group
            userData['admin'] = False
            usersDataBase.add2List(id, userData)
            return 'я запомнил, ты из группы ' + group + '\nтеперь можешь смотреть свое расписание (чекай help) или попроси у @eugene_programmist админку и сможешь его редактировать (!!!при смене группы админка теряется!!!)'
            
        elif msg == 'пн' or msg == 'понедельник':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Monday']
        elif msg == 'вт' or msg == 'вторник':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Tuesday']
        elif msg == 'ср' or msg == 'среда':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Wednesday']
        elif msg == 'чт'or msg == 'четверг':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Thursday']
        elif msg == 'пт' or msg == 'пятница':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Friday']
        elif msg == 'сб' or msg == 'суббота':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Saturday']
        elif msg == 'вс' or msg == 'воскресенье':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Sunday']

        elif msg == 'сегодня':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']][calendar.day_name[datetime.datetime.today().weekday()]]
        elif msg == 'завтра':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            today = datetime.date.today()
            tomorrow = datetime.date(today.year, today.month, today.day+1)
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            return scedullar[userData['group']][calendar.day_name[tomorrow.weekday()]]

        elif msg == 'неделя':
            if userData[userData['group']]['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            text = ''
            text += 'ПОНЕДЕЛЬНИК\n\n' + scedullar['Monday'] + '\n=========================\n\n'
            text += 'ВТОРНИК\n\n' + scedullar['Tuesday'] + '\n=========================\n\n'
            text += 'СРЕДА\n\n' + scedullar['Wednesday'] + '\n=========================\n\n'
            text += 'ЧЕТВЕРГ\n\n' + scedullar['Thursday'] + '\n=========================\n\n'
            text += 'ПЯТНИЦА\n\n' + scedullar['Friday'] + '\n=========================\n\n'
            text += 'СУББОТА\n\n' + scedullar['Saturday'] + '\n=========================\n\n'
            text += 'ВОСКРЕСЕНЬЕ\n\n' + scedullar['Sunday']
            return text

        elif msg.startswith('редактировать'):

            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'

            if not usersDataBase.getUserData(id)['admin']:
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
                del scedullar[userData['group']][weekday]
                scedullar[userData['group']][weekday] = new_text
                scedullar_update_str = json.dumps(scedullar, sort_keys=True, indent=4)
                with open('scedullar.json', 'w') as f:
                    f.write(scedullar_update_str)

            except BaseException:

                return 'случилась ошибка скажи одмену пустб починит'

            return 'проверять будеш?'

        elif msg.startswith('creategroup'):
            if not usersDataBase.getUserData(id)['admin']:
                return 'создавать группы могут толкьо админы'
            group = msg.split(' ')
            if len(group) != 2:
                print(group)
                return 'неправильная команда\nправилльно так:\creategroup 413'
            group = group[1]
            if not group.isdigit():
                return 'нужно написать номер группы (только цифры (тире тоже не надо, хотя откуда у тебя тире, ты шо, не из ммм, ты как меня нашел))'
            with open("scedullar.json", "r") as f:
                scedullar = json.load(f)
            scedullar[group] = scedullar['template']
            scedullar_update_str = json.dumps(scedullar, sort_keys=True, indent=4)
            with open('scedullar.json', 'w') as f:
                f.write(scedullar_update_str)
            return 'готово, обрадуй молодых'



        # BASE ANSWERS

        elif contain5(msg, ['как меня зовут']):
            return userData['firstname'] + ' ' + userData['secondname'] + '\nAKA: ' + userData['nick']

        elif msg.startswith('кто ты'):
            return choo5e([ 'да', 'тебя это ебать не должно', 'я?', 'я бот ашо', 'не важно кто, важно кто' ])

        if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам', 'добрый ', 'здравствуй' ]):
            return choo5e([ 'здарова, отец', 'привет', 'здарова заебал', 'как сам чел', 'Здравия желаю', 'Здравствуй, ' + userData['firstname'] ])
        if contain5(msg, [ 'пока', 'до связи', 'до завтра', 'досвидания', 'до свидания', 'пака' ]):
            return choo5e([ 'пака', 'пока(((', 'увидимся', 'до связи', 'было приятно пообщатсья', 'пока ' + userData['firstname'] ])

        elif msg.endswith('да'):
            return choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова', 'правильно' ])
        elif msg.endswith('нет'):
            return choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])
        elif endswith_list(msg, [ '[ff', 'хаа', 'хах', 'хвх', 'аха', 'хпх', 'хкх', 'hah', 'hhh', 'jaj', '[f[', 'хех', 'хых', 'а0а', 'фчф', 'ору', 'ржака', 'ржу', 'ржомба' ]):
            return choo5e([
                'РЖОМБА', 'Ебать я ору тоже', 'АХАХАХАХАХ))', 'Невероятная ржака', 'ахах)0',
                ')))))00))))))))))0))))))0))00000000)))))))))))))))))))))))0)0)0))0)0)0)))))',
                'лолирую', 'ржу уже третий день', 'Ржакаем всем сервером))0'
            ])
        elif end5(msg, [ 'але', 'ало', 'алло' ]):
            return choo5e([ 'да', 'да-да', 'але да', 'че', 'ты куда звонишь' ])

        elif msg == 'чел' or ((msg.startswith('че') and msg.endswith('ел'))):
            return 'ты'

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
