from os import truncate
from users_db import usersDataBase
from str_module import contain5, end5, i5, choo5e, endswith_list, _contain5, _end5, replace_layout, startswith_list, dicklist_search
from vars import public_email_pswrd, admin_id
from  help_msgs import constructHelpMsg
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
from scedullar import weekday_ru_en
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

# return reply for user accornding to message
def msgProc(id, msg, vksession, upload, fwdmsgs, peer_id):

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
                            return 'сам пошел нахуй'
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
                        return 'сам пошел нахуй'
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



        # USER DATA FUNCTIONS

        elif msg.startswith('сменить ник'):
            new_nick = msg.split(' ')[2]
            userData['nick'] = new_nick
            return 'изи'

        elif msg.startswith('setadmin'):
            if usersDataBase.getUserData(id)['admin'] < 100:
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
            if usersDataBase.getUserData(id)['admin'] < 100:
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
            return 'done'

        elif msg.startswith('permoban'):
            if usersDataBase.getUserData(id)['admin'] < 300:
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
            if usersDataBase.getUserData(id)['admin'] < 101:
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

        elif msg == 'update db':
            if usersDataBase.getUserData(id)['admin'] < 500:
                return 'действие доступно только админам лвла не ниже 500'
            usersDataBase.forceUpdate()
            return 'updated'
        elif msg == 'restore db':
            if usersDataBase.getUserData(id)['admin'] < 500:
                return 'действие доступно только админам лвла не ниже 500'
            usersDataBase.updateList()
            return 'restored'





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
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Monday']
        elif msg == 'вт' or msg == 'вторник':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Tuesday']
        elif msg == 'ср' or msg == 'среда':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Wednesday']
        elif msg == 'чт'or msg == 'четверг':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Thursday']
        elif msg == 'пт' or msg == 'пятница':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Friday']
        elif msg == 'сб' or msg == 'суббота':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Saturday']
        elif msg == 'вс' or msg == 'воскресенье':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']]['Sunday']

        elif msg == 'сегодня':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']][calendar.day_name[datetime.datetime.today().weekday()]]
        elif msg == 'завтра':
            if userData['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            today = datetime.date.today()
            tomorrow = datetime.date(today.year, today.month, today.day+1)
            with open('scedullar.json', 'r', encoding='utf-8') as f:
                scedullar = json.load(f)
            return scedullar[userData['group']][calendar.day_name[tomorrow.weekday()]]

        elif msg == 'неделя':
            if userData[userData['group']]['group'] == '':
                return 'сначала укажи свою группу (чекай команду help)'
            with open('scedullar.json', 'r', encoding='utf-8') as f:
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

                weekday = weekday_ru_en( commands[1] )
                if not weekday:
                    return 'неправильная команда'
                new_text = msg[ start_pointer+1 : len(msg) ]

                with open('scedullar.json', 'r', encoding='utf-8') as f:
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

        elif _contain5(msg, 'как') and _contain5(msg, 'дела'):
            return choo5e(['нормально, братик, у тебя как?', 'все круто, как у тебя', 'да вот\nработаю\nаты?'])

        elif msg.startswith('бот') or msg.endswith('бот'):
            return 'да я бот иче'

        elif msg.endswith('ты'):
            return 'кто'

        elif msg.startswith('правильно'):
            return 'спасибо брат'
        elif msg.startswith('спасибо' ) or msg.endswith('спасибо'):
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
        elif contain5(msg, [ 'уебок', 'уебан', 'мудак', 'гнида', 'хуесос', 'мудила', 'ебан', 'конченый', 'долбаеб', 'лох', 'дебил', 'дибил', 'пидор', 'пидр']):
            if contain5(msg, ['админ']):
                return 'бля, {}, сложно быть страшнее меня, но у твоей мамаши хорошо получается, уважаю, брат'.format(userData['firstname'])
            return choo5e([ 'ой да иди в пизду долбаеб блять', 'ебало закрой', msg, 'хули ты обзываешься пидорас', 'говоришь на меня переводишь на себя нахуй',
                'сам пидор', 'пошел нахуй', 'gjitk yf[eq', 'sosi', 'ты че сука', 'а по ебалу??' ])
        elif msg.find('ахуел') != -1 or msg.find('охуел') != -1:
            return choo5e([ 'сам охуел', 'а может ты охуел?', 'нет' ])
        elif msg.find('заебал') != -1:
            return choo5e([ 'сам заебал', 'это ты заебал' ])

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
