import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import time

# importing variables of bot init
from vars import group_token, debug, sleep_timeout, admin_token

# importing message pricessing function
from replies import msgProc

# importing users database module
import users_db

# for exception codes
# import socket, urllib3, requests


# getting api for connecting to my community
session = vk_api.VkApi(token = group_token)
api = session.get_api()
longpoll = VkLongPoll(session)
upload = VkUpload(session)

# session of mine to post in the wall
mysession = vk_api.VkApi(token=admin_token)
myapi = mysession.get_api()


# send message to id
def sendMsg(id, msg, attachments = ''):
    session.method('messages.send', { 'user_id': id, 'message': msg, 'random_id': 0, 'attachment': ','.join(attachments) })



# start console message
print('\n\n\nBot has been strted. Messages log:\n\n')


# db dumb timer
db_dubm_time = time.time()
# log onto db
users_db.updateList()


flag_run = True


while flag_run:


    # проверка вк на пидора
    try:

        # main loop
        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    
                    # get and convert message to lower case
                    msg = event.text.lower()
                    id = event.user_id
                    

                    # search user in json
                    userData = users_db.getUserData(id)
                    if not userData:
                        print('NEW USER\n')
                        # get sender name by id
                        response = api.users.get(user_ids = id)
                        name = [ str(response[0]['first_name']), str(response[0]['last_name']) ]
                        # save user data
                        userData = {
                            'name': name,
                            'admin': False,
                            'group': '',
                            'nick': name[0]
                        }
                        # save data in db
                        users_db.add2List(id, userData)
                        users_db.dumbList()


                    # processing the message
                    print(userData['name'][0], userData['name'][1], 'id=' + str(id))
                    print(time.ctime())
                    print(msg)

                    # turning bot off condition
                    if msg == 'стоп':
                        if userData['admin']:
                            sendMsg(id, 'ok')
                            users_db.dumbList()
                            flag_run = False
                            break
                        else:
                            attachments = []
                            attachments.append( 'photo-205950303_457239039' )
                            session.method('messages.send',
                                {
                                    'user_id': id,
                                    'message': 'ты не админ',
                                    'random_id': get_random_id(),
                                    'attachment': ','.join(attachments)
                                })
                            # image photo190344587_457278276

                    # get answer

                    if debug:

                        reply = msgProc(id, msg, session, myapi, upload)
                    
                    else:
                
                        try:
                            reply = msgProc(id, msg, session, myapi, upload)
                        except BaseException:
                            reply = 'ты блять его убил нахуй\nты его захуярил'
                            file = open('error_msgs.txt','a', encoding='utf-8')
                            file.write('///   NEW ERROR   ///\nMSG: "' + msg + '"\nTIME: ' + time.ctime() + '\n\n\n')
                            file.close()

                    # send it
                    if reply:
                        sendMsg(id, reply)
                        print('\nAnswered')

                    print('\n\n')


            # if (time.time() - db_dubm_time > 1800):
            #     users_db.dumbList()
            #     db_dubm_time = time.time()


            time.sleep(sleep_timeout)


    # if vk is gay then restart connection
    # errrs: socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout
    except BaseException:   # vashe poxui

        # getting api for connecting to my community
        session = vk_api.VkApi(token = group_token)
        api = session.get_api()
        longpoll = VkLongPoll(session)
        upload = VkUpload(session)

        # session of mine to post in the wall
        mysession = vk_api.VkApi(token=admin_token)
        myapi = mysession.get_api()
