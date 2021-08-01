from users_db import usersDataBase
from str_module import contain5, end5, i5, choo5e, endswith_list, _contain5, _end5, replace_layout
from vars import public_email_pswrd
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
    timeoutSec = 60


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


# return reply for user accornding to message
def msgProc(id, msg, vksession, upload):

    if msg != '':

        # get userdata from db
        userData = usersDataBase.getUserData(id)
        if not userData:
            return 'возникла ошибка при поиске вашей записи в базе данных, пожалуйста, сообщите админу\n@eugene_programmist'


        if  userData['admin'] < 0:
            return 'у тебя бан (навсегда)'
        if 'ban' in userData:
            if (time.time() - userData['ban']['start']) < (userData['ban']['time'] * 3600):
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

        elif msg.startswith('заспамить админа'):
            if msg[16] != '\n' and msg[17] != '\n':
                return 'неправильная команда (сообщение надо писать с новой строки)'
            sendEmail2Admin(id, msg[16:])
            return 'ваши замечания приняты, возможно, их прочитают'

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

        elif msg == 'help' or msg == 'команды' or msg == 'командв':
            return constructHelpMsg(userData['admin'])

        elif msg.startswith('переведи'):
            if msg[8] != '\n' and msg[9] != '\n':
                return 'неправильная команда (сообщение надо писать с новой строки)'
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
                msg += el['firstname'] + ' ' + el['secondname'] + ' aka: ' + el['nick'] + '\n'
            return msg

        elif msg == 'топ людей':
            list = usersDataBase.getSortedList(['firstname', 'secondname', 'msgCount'], 'msgCount', True)
            msg = 'топ 5 подпесчиков по количесву сообщений:\n\n'
            for el in list[0:5]:
                msg += str(el['msgCount']) + ':\n' + el['firstname'] + ' ' + el['secondname'][0] + '. @id' + str(el['id']) + '\n'
            return msg



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
        elif contain5(msg, [ 'пидор', 'пидр' ]):
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



        # GIVEAWAY CHEATS

        elif msg == 'буст сообщений':
            userData['ban'] = {
                'start': time.time(),
                'time': 10
            }
            return 'бан нахуй\nза читы'
        elif msg == 'буст сооьщений':
            return 'число ваших сообщений было увеличено на 1'

