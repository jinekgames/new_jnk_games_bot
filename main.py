import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import time

# importing variables of bot init
from vars import group_token, debug, sleep_timeout

# importing message pricessing function
from replies import msgProc


# getting api for connecting to my community
session = vk_api.VkApi(token = group_token)
api = session.get_api()
longpoll = VkLongPoll(session)


# send message to id
def sendMsg(id, msg):
    session.method('messages.send', { 'user_id': id, 'message': msg, 'random_id': 0 })


# main loop
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            
            # get and convert message to lower case
            msg = event.text.lower()
            id = event.user_id

            # processing the message
            print(msg)

            # turning bot off condition
            if msg == 'хватит нахуй':
                sendMsg(id, 'ok')
                break

            # get answer

            if debug:

                reply = msgProc(msg)
            
            else:
        
                try:
                    reply = msgProc(msg)
                except BaseException:
                    reply = 'ты блять его убил нахуй\nты его захуярил'
                    file = open('error_msgs.txt','a', encoding='utf-8')
                    file.write('///   NEW ERROR   ///\nMSG: "' + msg + '"\nTIME: ' + time.ctime() + '\n\n\n')
                    file.close()

            # send it
            if reply:
                sendMsg(id, reply)

    time.sleep(sleep_timeout)
