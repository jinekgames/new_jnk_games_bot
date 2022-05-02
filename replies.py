from os import truncate

from users_db import usersDataBase
from str_module import contain5, end5, i5, choo5e, endswith_list, _contain5, _end5, replace_layout, startswith_list, dicklist_search
from vars import public_email_pswrd, secret_msg_chance, bad_answ_prob
from  help_msgs import constructHelpMsg
from scedullar import weekday_ru_en, EVEN_WEEK_STR, NOT_EVEN_WEEK_STR

import time
import requests
import json
import datetime
import calendar
import smtplib

import random
random.seed(version=2)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import vk_api
from vk_api.utils import get_random_id


requestSession = requests.Session()


# some static variables
class SomeVars:
    timers = {}
    timeoutSec = 30
    chats = {}


def sendMsg2id(vksession, id, msg, attachments=[]):
    cur_time = time.time()
    if (not id in SomeVars.timers) or (cur_time - SomeVars.timers[id] > SomeVars.timeoutSec) or usersDataBase.getUserData(id)['admin'] > 500:
        SomeVars.timers[id] = cur_time
        rtrn_msg = ''
        try:
            vksession.get_api().messages.send(peer_id=id, message=msg, random_id=get_random_id(), attachment=attachments)
            rtrn_msg = 'готово, с вас three hundred bucks'
        except vk_api.exceptions.ApiError:
            rtrn_msg = 'сначала заставь его чтото написать боту хоть раз, чтобы бот смог отправить ему сообщение'
        return rtrn_msg
    else:
        return 'этому челу уже писали за последние 2 минуты'

def sendEmail2Admin(senderid, text):
    FROM  = "jnkgms.adm1n@gmail.com"
    TO    = "jnkgms.adm1n@gmail.com"
    PSWRD = public_email_pswrd

    msg = MIMEMultipart()
    msg['From']    = FROM
    msg['To']      = TO
    msg['Subject'] = 'BOT MESSAGE'
    body = 'From vk.com/id' + str(senderid) + '\n\nMessage:\n' + text
    msg.attach(MIMEText(body, 'plain'))

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(FROM, PSWRD)
    smtpObj.send_message(msg)

def loadPhoto2Vk(url, upload):
    image = requestSession.get(url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    return 'photo{}_{}'.format(photo['owner_id'], photo['id'])

def sendMsgWithPhoto(vksession, id, msg, url, upload):
    attachments = []
    attachments.append(loadPhoto2Vk(url, upload))
    vksession.get_api().messages.send(peer_id=id, message=msg, random_id=get_random_id(), attachment=attachments)

def sendAudio2id(vksession, peerId, trackOwnerId, trackId, msg=''):
    attachments = []
    attachments.append('audio{}_{}'.format(trackOwnerId, trackId))
    vksession.get_api().messages.send(peer_id=peerId, message=msg, random_id=get_random_id(), attachment=attachments)

def choo5eBySex(manVal, womanVal, man):
    if man:
        return manVal
    return womanVal

def randBadAnswer(answer, probability = bad_answ_prob):
    rand = random.randint(0, 100)
    if rand < probability:
        return answer
    return -1

def isWeekEven(date=datetime.date.today()) -> bool:
    return date.isocalendar()[1] % 2 == 0

# return reply for user accornding to message
def msgProc(id, msgReal: str, vksession, upload, fwdmsgs, peer_id):

    # convert message to lower case
    msg = msgReal.lower()

    # today date
    date = datetime.date
    # is week even param
    week_even_str = NOT_EVEN_WEEK_STR
    if isWeekEven(date.today()):
        week_even_str = EVEN_WEEK_STR


    inChat = False
    if not peer_id:
        peer_id = id
    else:
        inChat = True

    if msg != '':

        # get userdata from db
        userData = usersDataBase.getUserData(id)
        if not userData:
            return 'возникла ошибка при поиске вашей записи в базе данных, пожалуйста, сообщите админу\n@eugene_programmist'


        if  userData['admin'] < 0:
            sendMsgWithPhoto(vksession, id, '', 'https://sun9-58.userapi.com/impg/z_XjqSY_j1-YKatnrv3sjvGyUFc6MLd3TuOmig/yve7q3j0e8M.jpg?size=1080x791&quality=96&sign=287e6b6a0f789d3501f792ff5d66b8de&type=album', upload)
            return 'у тебя бан (навсегда)'
        if 'ban' in userData:
            if (time.time() - userData['ban']['start']) < (userData['ban']['time'] * 3600):
                sendMsgWithPhoto(vksession, id, '', 'https://sun9-58.userapi.com/impg/z_XjqSY_j1-YKatnrv3sjvGyUFc6MLd3TuOmig/yve7q3j0e8M.jpg?size=1080x791&quality=96&sign=287e6b6a0f789d3501f792ff5d66b8de&type=album', upload)
                return 'у тебя бан (соси)\nдо ' + time.ctime(userData['ban']['start']+userData['ban']['time'])

        
        
        # HUINYA

        rnd_int = random.randint(0, 1000)
        if rnd_int < secret_msg_chance:
            return choo5e([ 'мне похуй', 'много хочешь' ])

        if contain5(msg, [ 'поздравить', 'подравляю', 'поздравляю', 'с др' ]):
            if contain5(msg, [ 'данила', 'донила', 'даниила' ]):
                return sendMsg2id(vksession, 187191431, userData['firstname'] + ' поздравил тебя с др')
                """
                # vkBotSession of mine to post in the wall
                vkMySession = vk_api.VkApi(token=admin_token)
                vkMyApi = vkMySession.get_api()
                # это типа раньше он еще пост на стене дропал (чисток акпример тут пока будет)
                vkMyApi.wall.post(
                    owner_id = '-205950303',       # my id 190344587 community 205950303
                    from_group = 1,
                    message = 'ебать Данил с др нахуй\nОт: ' + userData['firstname'])
                """

        elif msg.startswith('послать'):
            if usersDataBase.getUserData(id)['admin'] < 7:
                return 'это действие могут выполнять только пользователи с уровнем не ниже 7'
            com = msg.split(' ')
            distId = com[1]
            if distId.isdigit():
                if len(distId) != 9:
                    return 'введите корректный айди чела которого надо послать'
                else:
                    userData_ = usersDataBase.getUserData(distId)
                    if userData_:
                        if userData_['admin'] > userData['admin'] and userData['admin'] < 500:
                            return choo5eBySex('сам пошел нахуй', 'сама пошла нахуй', userData['man'])
                        if not 'naxui' in userData_:
                            userData_['naxui'] = 1
                        else:
                            userData_['naxui'] += 1
                        if not 'naxui_ur' in userData:
                            userData['naxui_ur'] = 1
                        else:
                            userData['naxui_ur'] += 1
                    return sendMsg2id(vksession, distId, 'ктото послал тебя нахуй')
            else:
                if len(com) < 3:
                    return 'надо указать и имя и фамилию прям как в вк'
                distId = usersDataBase.findIdByFieldS(['firstname', 'secondname'], [com[1], com[2]])
                if distId:
                    userData_ = usersDataBase.getUserData(distId)
                    if userData_['admin'] > userData['admin'] and userData['admin'] < 500:
                        return choo5eBySex('сам пошел нахуй', 'сама пошла нахуй', userData['man'])
                    if not 'naxui' in userData_:
                        userData_['naxui'] = 1
                    else:
                        userData_['naxui'] += 1
                    if not 'naxui_ur' in userData:
                        userData['naxui_ur'] = 1
                    else:
                        userData['naxui_ur'] += 1
                    return sendMsg2id(vksession, distId, 'ктото послал тебя нахуй')
                else:
                    return 'я его(ее) не нашел'

        elif msg.startswith('позвать бухать'):
            if usersDataBase.getUserData(id)['admin'] < 6:
                return 'это действие могут выполнять только пользователи с уровнем не ниже 6'
            com = msg.split(' ')
            distId = com[2]
            if distId.isdigit():
                if len(distId) != 9:
                    return 'введите корректный айди чела которого надо послать'
                else:
                    return sendMsg2id(vksession, distId, 'ктото позвал тебя бухать')
            else:
                distId = usersDataBase.findIdByFieldS(['firstname', 'secondname'], [com[2], com[3]])
                if distId:
                    return sendMsg2id(vksession, distId, 'ктото позвал тебя бухать')
                else:
                    return 'я его(ее) не нашел'

        elif msg.startswith('написать'):
            if usersDataBase.getUserData(id)['admin'] < 1:
                return 'это действие могут выполнять только пользователи с уровнем не ниже 1'
            msg_start = msg.find('\n')
            msg_split_command = msg.split('\n')[0].split(' ')
            if len(msg_split_command) < 3 or msg_start == -1:
                return 'чел ты...\nнеправильно составил команду\nнадо так:\n\nотправить женя калинин\nчел ты гений'
            distId = usersDataBase.findIdByFieldS(['firstname', 'secondname'], [msg_split_command[1], msg_split_command[2]])
            if not distId:
                return 'я его(ее) не нашел'
            msg_text = msg[msg_start:]
            if usersDataBase.getUserData(distId)['admin'] > 500:
                if contain5(msg_text, [ 'иди', 'пошел', 'пашел', 'пашол', 'пашол', 'пошол', 'пошёл', 'gjitk' ]) and contain5(msg_text, [ 'хуй', 'пизду', '[eq' ]) or \
                    msg_text.find('соси') != -1 or contain5(msg_text, [ 'пидор', 'пидр' ]) or \
                    contain5(msg_text, [ 'уебок', 'уебан', 'мудак', 'гнида', 'хуесос', 'мудила', 'конченый', 'долбаеб', 'лох', 'хуйня', 'хуесос', 'блядина', 'чмо' ]):
                        return 'ты такие слова админу не говори'
            if len(msg_split_command) > 3 and msg_split_command[3] == 'анон':
                text = msg_text
            else:
                text = userData['firstname'] + ' оставил тебе сообщение:\n' + msg_text
            return sendMsg2id(vksession, distId, text)

        elif msg.startswith('заспамить админа'):
            if msg[16] != '\n' and msg[17] != '\n':
                return 'неправильная команда (сообщение надо писать с новой строки)'
            sendEmail2Admin(id, msg[16:])
            return 'ваши замечания приняты, возможно, их прочитают'

        elif msg.startswith('idbyname'):
            return '@id' + str(usersDataBase.findIdByFieldS(['firstname', 'secondname'], [msg.split(' ')[1], msg.split(' ')[2]]))

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

                sendMsg2id(vksession, peer_id, text, ','.join(attachments))

                return -1

            elif text:
                sendMsg2id(vksession, peer_id, text)

                return -1

            elif wiki:
                return response.get('AbstractURL')

            else:
                return 'нихуя не нашлось'

        elif msg == 'джони' or msg == 'джонни' or msg == 'johny' or msg == 'johnny':
            with open('additional_data/johny.json', 'r', encoding='utf-8') as f:
                url = choo5e(json.load(f)['list'])
            sendMsgWithPhoto(vksession, peer_id, '', url, upload)
            return -1

        if msg == 'какое я волокно':
            if not 'volokno' in userData:
                userData['volokno'] = random.randint(0, 1)
            if userData['volokno']:
                return 'сжатое'
            else:
                return 'растянутое'


        elif msg == 'help' or msg == 'команды' or msg == 'командв':
            return constructHelpMsg(userData['admin'])

        elif msg.startswith('переведи'):
            if fwdmsgs:
                text = ''
                for msg in fwdmsgs:
                    text += replace_layout(msg) + '\n\n'
                return text
            if msg[8] != '\n' and msg[9] != '\n':
                return 'неправильная команда (сообщение надо писать с новой строки или пересылать чьето сообщение)'
            return replace_layout(msg[9:])

        elif i5(msg, ['анекдот', 'шутка', 'разрывная']):
            with open('additional_data/jokes.json', 'r', encoding='utf-8') as f:
                return choo5e(json.load(f)['list'])
                
        elif msg == 'гачи топ':
            with open('additional_data/gachi.json', 'r', encoding='utf-8') as f:
                return choo5e(json.load(f)['list'])

        elif msg.startswith('вероятность'):
            a = msg.find('что')
            if a > 0:
                return 'вероятность того, что' + msg[ a + 3 : ] + ' составляет ' + str(random.randint( 1, 99 )) + '%'
            return 'вероятность того, что' + msg[ 11 : ] + ' составляет ' + str(random.randint( 1, 99 )) + '%'
        
        elif msg.startswith('выбери'):
            cases = msg.split('\n')
            return cases[random.randint( 1, len(cases) - 1 )]

        elif msg == 'список людей':
            list = usersDataBase.getSortedList(['firstname', 'secondname', 'nick'], 'firstname')
            msg = ''
            for el in list:
                if el['firstname'] == 'bot':
                    continue
                msg += 'id ' + el['id'] + '\n' + el['firstname'] + ' ' + el['secondname'] + ' aka: ' + el['nick'] + '\n'
            return msg

        elif msg == 'топ людей':

            list = usersDataBase.getSortedList(['firstname', 'secondname', 'msgCount'], 'msgCount', True)
            msg = 'топ 5 подпесчиков по количесву сообщений:\n\n'
            for el in list[0:5]:
                msg += str(el['msgCount']) + ':\n' + el['firstname'] + ' ' + el['secondname'][0] + '. @id' + str(el['id']) + '\n'
                
            list = usersDataBase.getSortedList(['firstname', 'secondname', 'naxui_ur'], 'naxui_ur', True)
            msg += '\n\nтоп 5 подпесчиков по количесву посыланий:\n\n'
            for el in list[0:5]:
                msg += '~' + str(int(el['naxui_ur'] / 10) * 10) + ':\n' + el['firstname'] + ' ' + el['secondname'][0] + '. @id' + str(el['id']) + '\n'
            return msg

        elif msg == 'начать':
            return 'привет!\nчтобы посмотреть список доступных команд напиши help или команды'

        # ВЯЛЫЕЕ КОМАНДЫ

        elif msg == 'шеф' or msg == 'шэф':
            return '@all\nШЕФ В ДС'

        elif msg == '89':
            return '@all\nВСЕ К ДК'

        elif msg.startswith('кто мы'):
            if 'abils' in userData and 'vyalyi' in userData['abils']:
                return 'ВЯЛЫЕ ПИТОНЫ!!1!!1'

        elif msg.startswith('чего мы хотим'):
            if 'abils' in userData and 'vyalyi' in userData['abils']:
                return 'ВЛАСТИ ОСТРЫХ КОЗЫРЬКОВ!!!!!1!!!!'

        elif contain5(msg, ['бан', 'кик']) and not contain5(msg, ['не бан', 'не кик', 'разбан']):
            if 'abils' in userData and 'vyalyi' in userData['abils']:
                return 'По приказу Острых Козырков'
            elif userData['admin'] < 10:
                return 'ты че ахуел мы тя самого ща забаним нахуй'

        elif _contain5(msg, 'контейнер'):
            return 'насрал в контейнер'



        # USER DATA FUNCTIONS

        elif msg.startswith('сменить ник'):
            new_nick = msg.split(' ')[2]
            userData['nick'] = new_nick
            return 'изи'

        elif msg.startswith('setadmin'):
            if userData['admin'] < 100:
                return 'назначать админов могут толкьо админы лвлом не ниже 100'

            cmds = msg.split(' ')
            if len(cmds) != 3:
                return 'неверная команда, надо так \nmakeadmin 34019628 1'
            if not cmds[2].isdigit():
                return 'уровень доступа надо указать числом от -1 до 999'
            lvl_ = int(cmds[2])
            if lvl_ > userData['admin'] or lvl_ < 0:
                return 'можно назначить толкьо на уровень не выше своего'
            userData_ = usersDataBase.getUserData(cmds[1])
            if not userData_:
                return '404 user not found'
            if userData_['admin'] < 0:
                return 'из пермобана вернуть нельзя'
            if userData_['admin'] > lvl_ and userData['admin'] < 101:
                return 'занижать админку могут только админы начиная со 101 лвла'
            userData_['admin'] = lvl_
            return 'done'

        elif msg.startswith('ban'):
            if userData['admin'] < 100:
                return 'банить могут только админы лвла не ниже 100'

            comands = msg.split(' ')
            if len(comands) != 3:
                return 'incorrect sintaxys'
            if not comands[2].isdigit():
                return 'incorrect sintaxys'
            userData_ = usersDataBase.getUserData(comands[1])
            if not userData_:
                return 'user not found'
            userData_['ban'] = {
                'start': time.time(),
                'time': int(comands[2])
            }
            userData_['admin'] = False
            return 'ПО ПРИКАЗУ ОСТРЫХ КОЗЫРЬКОВ'

        elif msg.startswith('permoban'):
            if userData['admin'] < 300:
                return '(с)перма банить могут только админы лвла не ниже 300'

            comands = msg.split(' ')
            if len(comands) != 2:
                return 'incorrect sintaxys'
            userData_ = usersDataBase.getUserData(comands[1])
            if not userData_:
                return 'user not found'
            userData_['ban'] = {
                'start': time.time(),
                'time': -1
            }
            userData_['admin'] = -1
            return 'done\nесли что его больше не вернуть (никак)'

        elif msg.startswith('unban'):
            if userData['admin'] < 101:
                return 'разбанить могут только админы лвла не ниже 101'

            distId = msg.split(' ')
            if len(distId) != 2:
                return 'incorrect sintaxys'
            distId = distId[1]
            userData_ = usersDataBase.getUserData(distId)
            if not userData_:
                return 'user not found'
            userData_['ban']['time'] = 0
            return 'done'

        elif msg.startswith('setvyalyi'):
            if userData['admin'] < 500 and ( userData['admin'] < 100 or (not 'abils' in userData) and (not 'vyalyi' in userData['abils']) ):
                return 'принять в банду могут только вялые админы лвла не ниже 100'

            distId = msg.split(' ')
            if len(distId) != 2:
                return 'incorrect sintaxys'
            distId = distId[1]
            userData_ = usersDataBase.getUserData(distId)
            if not userData_:
                return 'user not found'
            if not 'abils' in userData_:
                userData_['abils'] = {}
            userData_['abils']['vyalyi'] = 'yes'
            return 'ПО ПРИКАЗУ ОСТРЫХ КОЗЫРЬКОВ'

        elif msg.startswith('delvyalyi'):
            if userData['admin'] < 500 and ( userData['admin'] < 100 or (not 'abils' in userData) and (not 'vyalyi' in userData['abils']) ):
                return 'исключить из банды могут только вялые админы лвла не ниже 100'

            distId = msg.split(' ')
            if len(distId) != 2:
                return 'incorrect sintaxys'
            distId = distId[1]
            userData_ = usersDataBase.getUserData(distId)
            if not userData_:
                return 'user not found'
            if 'abils' in userData_:
                if 'vyalyi' in userData_['abils']:
                    del userData_['abils']['vyalyi']
            return 'ПО ПРИКАЗУ ОСТРЫХ КОЗЫРЬКОВ'

        elif msg.startswith('userdata'):
            if userData['admin'] < 100:
                return 'функция доступна только пользователям с уровнем не ниже 100'
            distId = msg.split(' ')[1]
            userData_ = usersDataBase.getUserData(distId)
            text = userData_['firstname'] + ' ' + userData_['secondname'] + '\nAKA: ' + userData_['nick'] + \
                '\nотправил боту ' + str(userData_['msgCount']) + ' сообщений(е)'
            if 'man' in userData_:
                text += '\nмужчина: ' + choo5eBySex('да', 'нет', userData_['man'])
            if len(userData_['group']) > 0:
                text += '\nгруппа: ' + userData_['group']
            if userData_['admin']:
                text += '\nправа админа: ' + str(userData_['admin'])
            if 'ban' in userData_:
                text += '\nбыл бан ' + time.ctime(userData_['ban']['start'])
            if 'naxui_ur' in userData_:
                text += '\nпосылал ' + str(userData_['naxui_ur']) + ' раз'
            if 'naxui' in userData_:
                text += '\nпытались послать ' + str(userData_['naxui']) + ' раз(а)'
            return text

        elif msg == 'update db':
            if userData['admin'] < 500:
                return 'действие доступно только админам лвла не ниже 500'
            usersDataBase.forceUpdate()
            return 'updated'
        elif msg == 'restore db':
            if userData['admin'] < 500:
                return 'действие доступно только админам лвла не ниже 500'
            usersDataBase.updateList()
            return 'restored'

        elif msg.startswith('updatefield'):
            if userData['admin'] < 500:
                return 'действие доступно только админам лвла не ниже 500'
            field = msg.split(' ')[1]

            if field == 'sex':

                vkapi = vksession.get_api()
                def foo(id):
                    vksex = vkapi.users.get(user_ids=id, fields='sex')[0]['sex']
                    if vksex == 1:
                        return False
                    return True

                usersDataBase.updateFieldByFooOfId('man', foo)
                return 'ok'

            return 'incorrect command'




        # SHARAGA

        elif msg.startswith('группа'):
            group = msg.split(' ')
            if len(group) != 2:
                print(group)
                return 'неправильная команда\nправилльно так:\nгруппа 381904'
            group = group[1]
            if not group.isdigit():
                return 'нужно написать номер группы (только цифры (тире тоже не надо, хотя откуда у тебя тире, ты шо, не из ммм, ты как меня нашел))'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if not group in scedullar:
                return 'такой группы еще нет в боте, попроси @eugene_programmist добавить твою группу'
            userData['group'] = group
            if userData['admin'] < 30:
                userData['admin'] = 9
            return 'я запомнил, ты из группы ' + group + '\nтеперь можешь смотреть свое расписание (чекай help) или попроси у @eugene_programmist или другого админа ранга не ниже модера модерку и сможешь его редактировать (!!!при смене группы модерка теряется!!!)'
            
        elif msg == 'пн' or msg == 'понедельник':
            day_str = 'Monday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'вт' or msg == 'вторник':
            day_str = 'Tuesday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'ср' or msg == 'среда':
            day_str = 'Wednesday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'чт'or msg == 'четверг':
            day_str = 'Thursday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'пт' or msg == 'пятница':
            day_str = 'Friday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'сб' or msg == 'суббота':
            day_str = 'Saturday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'вс' or msg == 'воскресенье':
            day_str = 'Sunday'
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]

        elif msg == 'сегодня':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            day_str = calendar.day_name[datetime.datetime.today().weekday()]
            if day_str + week_even_str in scedullar[userData['group']]:
                day_str += week_even_str
            return scedullar[userData['group']][day_str]
        elif msg == 'завтра':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            today = datetime.date.today()
            tomorrow = datetime.date(today.year, today.month, today.day + 1)
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            day_str = calendar.day_name[tomorrow.weekday()]
            # use another param cos tomorrow mb the other week
            next_week_even_str = NOT_EVEN_WEEK_STR
            if isWeekEven(tomorrow):
                next_week_even_str = EVEN_WEEK_STR
            if day_str + next_week_even_str in scedullar[userData['group']]:
                day_str += next_week_even_str
            return scedullar[userData['group']][day_str]

        # TODO:
        # elif msg == 'сегодня':
        #     if userData['group'] == '':
        #         return 'сначала укажи свою группу (чекай команду help)'
        #     with open('scedullar.json', 'r', encoding='utf-8') as f:
        #         scedullar = json.load(f)
        #     day_str = calendar.day_name[today.weekday()]
        #     # #
        #     # week_even_str = NOT_EVEN_WEEK_STR
        #     # if isWeekEven(today):
        #     #     week_even_str = EVEN_WEEK_STR
        #     # if day_str + week_even_str in scedullar[userData['group']]:
        #     #     day_str += week_even_str

        #     print(week_even_str)

        #     # return scedullar[userData['group']][day_str]

        #     if day_str + week_even_str in scedullar[userData['group']]:
        #         day_str += week_even_str
        #     return scedullar[userData['group']][day_str]
        # elif msg == 'завтра':
        #     if userData['group'] == '':
        #         return 'сначала укажи свою группу (чекай команду help)'
        #     with open('scedullar.json', 'r', encoding='utf-8') as f:
        #         scedullar = json.load(f)
        #     tomorrow = (date + 1).today()
        #     day_str = calendar.day_name[tomorrow.weekday()]
        #     # use another param cos tomorrow mb the other week
        #     next_week_even_str = NOT_EVEN_WEEK_STR
        #     if isWeekEven(tomorrow):
        #         next_week_even_str = EVEN_WEEK_STR
        #     if day_str + next_week_even_str in scedullar[userData['group']]:
        #         day_str += next_week_even_str

        #     print(week_even_str)
            
        #     return scedullar[userData['group']][day_str]


        elif msg == 'расписание':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if userData['group'] in scedullar:
                scedullar = scedullar[userData['group']]
            else:
                return 'твоей группы пока нет в расписании, обратись к админу сообщества'
            text = '//////////////////////////////////////////////\n\n'
            for day in [
                ['ПОНЕДЕЛЬНИК\n\n', 'Monday'    ],
                ['ВТОРНИК\n\n',     'Tuesday'   ],
                ['СРЕДА\n\n',       'Wednesday' ],
                ['ЧЕТВЕРГ\n\n',     'Thursday'  ],
                ['ПЯТНИЦА\n\n',     'Friday'    ],
                ['СУББОТА\n\n',     'Saturday'  ],
                ['ВОСКРЕСЕНЬЕ\n\n', 'Sunday'    ],
            ]:
                text += day[0]
                if day[1] + EVEN_WEEK_STR in scedullar and day[1] + NOT_EVEN_WEEK_STR in scedullar:
                    text += "ЧЕТНАЯ\n\n"   + scedullar[day[1] + EVEN_WEEK_STR] + "\n\n----------------------------------------------\n\n"
                    text += "НЕЧЕТНАЯ\n\n" + scedullar[day[1] + NOT_EVEN_WEEK_STR]
                else:
                    text += scedullar[day[1]]
                text += '\n\n//////////////////////////////////////////////\n\n'
                
            return text

        elif msg == 'неделя':
            if isWeekEven():
                return 'четная'
            return 'нечетная'


        elif msg.startswith('редактировать') or msg.startswith('редактирвоать'):

            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'

            if usersDataBase.getUserData(id)['admin'] < 10:
                return 'менять расписание могут только модеры'

            try:

                commands = msg.split('\n')
                start_pointer = len(commands[0])
                if len(commands) < 2:
                    return 'неправильная команда'
                commands = commands[0].split(' ')
                if len(commands) < 2:
                    return 'неправильная команда'

                weekday = weekday_ru_en(commands[1])
                if not weekday:
                    return 'неправильная команда'
                new_day_str = msgReal[start_pointer + 1: ]

                with open('scedullar.json', 'r', encoding='utf-8') as f:
                    scedullar = json.load(f)
                
                # we have week even param
                if len(commands) > 2 and commands[2] != '':
                    even_param = EVEN_WEEK_STR
                    if commands[2] == 'неч':
                        even_param = NOT_EVEN_WEEK_STR
                    weekday += even_param
                else:
                    if weekday + EVEN_WEEK_STR in scedullar[userData['group']]:
                        del scedullar[userData['group']][weekday + EVEN_WEEK_STR]
                    if weekday + NOT_EVEN_WEEK_STR in scedullar[userData['group']]:
                        del scedullar[userData['group']][weekday + NOT_EVEN_WEEK_STR]

                if weekday in scedullar[userData['group']]:
                    del scedullar[userData['group']][weekday]
                scedullar[userData['group']][weekday] = new_day_str
                scedullar_update_str = json.dumps(scedullar, sort_keys=True, indent=4)
                with open('scedullar.json', 'w') as f:
                    f.write(scedullar_update_str)

            except BaseException:

                return 'случилась ошибка скажи одмену пустб починит'

            return 'проверять будеш?'

        elif msg.startswith('creategroup'):
            if usersDataBase.getUserData(id)['admin'] < 30:
                return 'создавать группы могут только админы рангом не ниже 30'
            group = msg.split(' ')
            if len(group) != 2:
                print(group)
                return 'неправильная команда\nправилльно так:\creategroup 413'
            group = group[1]
            if not group.isdigit():
                return 'нужно написать номер группы (только цифры (тире тоже не надо, хотя откуда у тебя тире, ты шо, не из ммм, ты как меня нашел))'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            if group in scedullar:
                return 'группа с таким ноером уже существует'
            scedullar[group] = scedullar['template']
            scedullar_update_str = json.dumps(scedullar, sort_keys=True, indent=4)
            with open('scedullar.json', 'w') as f:
                f.write(scedullar_update_str)
            return 'готово, обрадуй молодых'



        # BASE ANSWERS

        elif contain5(msg, ['мои данные']):
            text = userData['firstname'] + ' ' + userData['secondname'] + '\nAKA: ' + userData['nick'] + \
                '\nты отправил боту ' + str(userData['msgCount']) + ' сообщений(е)'
            if 'man' in userData:
                text += '\nмужчина: ' + choo5eBySex('да', 'нет', userData['man'])
            if 'abils' in userData:
                if 'vyalyi' in userData['abils']:
                    text += '\nсостоит в клубе вялые питоны'
            if len(userData['group']) > 0:
                text += '\nтвоя группа: ' + userData['group']
            if userData['admin']:
                text += '\nправа админа: ' + str(userData['admin'])
            if 'ban' in userData:
                text += '\nбыл бан ' + time.ctime(userData['ban']['start'])
            if 'naxui_ur' in userData:
                text += '\nты посылал ' + str(userData['naxui_ur']) + ' раз'
            if 'naxui' in userData:
                text += '\nтебя пытались послать ' + str(userData['naxui']) + ' раз(а)'
            return text

        elif msg.startswith('кто ты'):
            return choo5e([ 'да', 'тебя это ебать не должно', 'я?', 'я бот ашо', 'не важно кто, важно кто' ])

        if contain5(msg, [ 'привет', 'даров', 'hi', 'hello', 'шалом', 'салам', 'добрый ', 'здравствуй' ]):
            return choo5e([ 'здарова, отец', 'привет', 'здарова заебал', 'как сам чел', 'Здравия желаю', 'Здравствуй, ' + userData['firstname'] ])
        if contain5(msg, [ 'пока', 'до связи', 'до завтра', 'досвидания', 'до свидания', 'пака' ]):
            return choo5e([ 'пака', 'пока(((', 'увидимся', 'до связи', 'было приятно пообщатсья', 'пока ' + userData['firstname'] ])

        elif msg.endswith('да'):
            answ = choo5e([ 'пизда', 'манда', 'провода', 'поезда', 'пидора слова', 'правильно' ])
            if inChat:
                return randBadAnswer(answ)
            return answ
        elif msg.endswith('нет'):
            answ = choo5e([ 'пидора ответ', 'минет', 'шлюхи аргумент' ])
            if inChat:
                return randBadAnswer(answ)
            return answ
        elif endswith_list(msg, [ '[ff', 'хаа', 'хах', 'хвх', 'аха', 'хпх', 'хкх', 'hah', 'hhh', 'jaj', '[f[', 'хех', 'хых', 'а0а', 'фчф', 'ору', 'ржака', 'ржу', 'ржомба' ]):
            answ = choo5e([
                'РЖОМБА', 'Ебать я ору тоже', 'АХАХАХАХАХ))', 'Невероятная ржака', 'ахах)0',
                ')))))00))))))))))0))))))0))00000000)))))))))))))))))))))))0)0)0))0)0)0)))))',
                'лолирую', 'ржу уже третий день', 'Ржакаем всем сервером))0'
            ])
            if inChat:
                return randBadAnswer(answ)
            return answ
        elif end5(msg, [ 'але', 'ало', 'алло' ]):
            return choo5e([ 'да', 'да-да', 'але да', 'че', 'ты куда звонишь' ])

        elif msg == 'чел' or ((msg.startswith('че') and msg.endswith('ел'))):
            return 'ты'

        elif _contain5(msg, 'как') and _contain5(msg, 'дела'):
            return choo5e(['нормально, братик, у тебя как?', 'все круто, как у тебя', 'да вот\nработаю\nаты?'])

        elif msg.startswith('бот') or msg.endswith('бот'):
            return 'да я бот иче'

        elif msg.endswith('ты'):
            return 'кто'

        elif msg.startswith('правильно'):
            return 'спасибо брат'
        elif msg.startswith('спасибо' ) or msg.endswith('спасибо'):
            return choo5e([ choo5eBySex('обращайся, братик', 'обращайся, сестренка', userData['man']), 'пожалуйста' ])
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
        elif contain5(msg, [ 'иди', 'пошел', 'пашел', 'пашол', 'пашол', 'пошол', 'пошёл', 'gjitk' ]) and contain5(msg, [ 'хуй', 'пизду', '[eq' ]):
            return choo5e([ choo5eBySex('сам иди', 'сама иди', userData['man']), choo5eBySex('пошел нахуй', 'пошла нахуй', userData['man']), 'gjitk yf[eq', 'sosi', 'ты че сука', 'а может ты?' ])
        elif msg.find('соси') != -1 :
            return choo5e([ choo5eBySex('сам соси сука', 'обидно', userData['man']), 'иди нахуй пидорас', 'чекай мать' ])
        elif msg.find('мать') != -1 :
            return choo5e([ 'серьезно чел, шутки про мать в ' + str( datetime.date.today().year ) ])
        elif msg.find('жир') != -1 :
            return choo5e([ 'не жир, а силовая броня' ])
        elif msg.find('резня') != -1 :
            return 'РЕЗНЯЯЯЯЯЯЯЯЯ'
        elif msg.find('гном') != -1 :
            return 'гном тут только ты'    
        elif contain5(msg, [ 'уебок', 'уебан', 'мудак', 'гнида', 'хуесос', 'мудила', 'ебан', 'конченый', 'долбаеб', 'лох', 'дебил', 'дибил', 'пидор', 'пидр']):
            if contain5(msg, ['админ']):
                return 'бля, {}, сложно быть страшнее меня, но у твоей мамаши хорошо получается, уважаю, брат'.format(userData['firstname'])
            return choo5e([ 'ой да иди в пизду долбаеб блять', 'ебало закрой', msg, 'хули ты обзываешься пидорас', 'говоришь на меня переводишь на себя нахуй',
                'сам пидор', 'пошел нахуй', 'gjitk yf[eq', 'sosi', 'ты че сука', 'а по ебалу??' ])
        elif msg.find('ахуел') != -1 or msg.find('охуел') != -1:
            return choo5e([ 'сам охуел', 'а может ты охуел?', 'нет' ])
        elif msg.find('заебал') != -1:
            return choo5e([ choo5eBySex('сам заебал', 'сама заебала', userData['man']), choo5eBySex('это ты заебал', 'это ты заебала', userData['man']) ])
        elif msg.find('молчать') != -1 and msg.find('машина') != -1:
            return 'ебало офф'

        elif msg == 'amogus' or msg == 'амогус' or msg == 'абоба' or msg == 'aboba':
            amogus = {
                'id': '456241722',
                'owner_id': '133887163',
            }
            print(peer_id)
            sendAudio2id(vksession, peer_id, amogus['owner_id'], amogus['id'])
            return -1



        # STUPID DIALOGS

        elif _contain5(msg, 'кто спрашивает'):
            return 'ну я спрашиваю'
        elif _contain5(msg, 'я спрашиваю'):
            return 'кто я?'
        elif _contain5(msg, 'кто я'):
            return 'смотря кто спрашивает'



        # GIVEAWAY CHEATS

        elif msg == 'буст сообщений':
            userData['ban'] = {
                'start': time.time(),
                'time': 10
            }
            return 'бан нахуй\nза читы'
        elif msg == 'буст сооьщений':
            return 'число ваших сообщений было увеличено на 1'



        # start commands

        elif startswith_list(msg, ['start', 'старт']):
            
            commands = msg.split(' ')

            if i5(commands[1], ['мафия', 'mafia']):
                
                if not inChat:
                    return 'команда доступна тольkо для чатов'

                if peer_id in SomeVars.chats:
                    return 'сначала закончите ' + SomeVars.chats[peer_id]['action']

                SomeVars.chats[peer_id] = {
                    'action': 'mafia',
                    'starttime': time.time(),
                    'roles_start': 0
                }

                return 'введите роли и количество игроков построчно типо такого (если какойто роли не надо, то ее писать не надо):\n\nмафия 1\nмирный 3\nмедик 1\nкомиссар 1'

        elif startswith_list(msg, ['end', 'закончить']):
            
            commands = msg.split(' ')

            if i5(commands[1], ['мафия', 'mafia']):
                
                if not inChat:
                    return 'команда доступна тольkо для чатов'

                SomeVars.chats.pop(peer_id)

                return 'действие завершено'


        elif inChat:

            if peer_id in SomeVars.chats:
                if (time.time() - SomeVars.chats[peer_id]['starttime']) < 86400:

                    info = SomeVars.chats[peer_id]

                    if info['action'] == 'mafia':

                        if info['roles_start'] == 0:
                            commands = msg.split('\n')
                            info['roles_start'] = []
                            info['players'] = []
                            for role in commands:
                                role_splitted = role.split(' ')
                                for i in range(int(role_splitted[1])):
                                    info['roles_start'].append(role_splitted[0])
                            return 'теперь пишете "я" и бот скинет вам вашу роль'

                        elif msg == 'я' and info['roles_start']:

                            if not info['roles_start']:
                                return 'все роли уже раздали'
                            print(info['players'])
                            print(id)
                            if dicklist_search(info['players'], 'id', id) > -1:
                                return 'у тебя уже есть роль, чекай лс'

                            role_num = random.randint(0, len(info['roles_start']) - 1)
                            role = info['roles_start'][role_num]
                            info['roles_start'].pop(role_num)
                            info['players'].append({
                                'id': id,
                                'name': userData['firstname'] + ' ' + userData['secondname'],
                                'role': role
                            })

                            sendMsg2id(vksession, id, role)
                            if not info['roles_start']:
                                SomeVars.chats.pop(peer_id)
                                return 'это все'
                            return -1
