import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

import time

# importing variables of bot init
from vars import group_token, debug, sleep_timeout, admin_token

# importing message pricessing function
from replies import msgProc


# getting api for connecting to my community
session = vk_api.VkApi(token = group_token)
api = session.get_api()
longpoll = VkLongPoll(session)
upload = VkUpload(session)

# session of mine to post in the wall
mysession = vk_api.VkApi(token=admin_token)
myapi = mysession.get_api()


# send message to id
def sendMsg(id, msg):
    session.method('messages.send', { 'user_id': id, 'message': msg, 'random_id': 0 })



# start console message
print('\n\n\nBot has been strted. Messages log:\n\n')

# main loop
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            
            # get and convert message to lower case
            msg = event.text.lower()
            id = event.user_id

            # get sender name by id
            response = api.users.get(user_ids = id)
            name = [ response[0]['first_name'], response[0]['last_name'] ]

            # processing the message
            print(name[0], name[1], 'id=' + str(id))
            print(time.ctime())
            print(msg)

            # turning bot off condition
            if msg == '3348':
                sendMsg(id, 'ok')
                break

            # get answer

            if debug:

                reply = msgProc(id, msg, session, myapi, upload, name)
            
            else:
        
                try:
                    reply = msgProc(id, msg, session, myapi, upload, name)
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

    time.sleep(sleep_timeout)
