import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

import time

import json

# importing variables of bot init
from vars import group_token, debug, sleep_timeout, admin_token

# importing message pricessing function
from replies import msgProc

# importing users database module
import users_db


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


# open json users list
with open("users.json", "r") as f:
    userslist = json.load(f)


# db dumb timer
db_dubm_time = time.ctime()


# main loop
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            
            # get and convert message to lower case
            msg = event.text.lower()
            id = event.user_id


            # get sender name by id
            response = api.users.get(user_ids = id)
            name = [ str(response[0]['first_name']), str(response[0]['last_name']) ]
            

            # search user in json
            if not (str(id) in userslist):
                print('NEW USER\n')
                userslist[str(id)] = {
                    'name': name,
                    'admin': False,
                    'group': '',
                    'nick': name[0]
                }


            # processing the message
            print(name[0], name[1], 'id=' + str(id))
            print(time.ctime())
            print(msg)

            # turning bot off condition
            if msg == '3348':
                sendMsg(id, 'ok')

                userslist_update_str = json.dumps(userslist, sort_keys=True, indent=4)
                print('\n\n', userslist_update_str, '\n\n\n\n')
                with open('users.json', 'w') as f:
                    f.write(userslist_update_str)
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


    if (time.ctime() - db_dubm_time > 1800):
        userslist_update_str = json.dumps(userslist, sort_keys=True, indent=4)
        print('\n\n', userslist_update_str, '\n\n\n\n')
        with open('users.json', 'w') as f:
            f.write(userslist_update_str)


    time.sleep(sleep_timeout)
