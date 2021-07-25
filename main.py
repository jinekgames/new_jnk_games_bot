from users_db import usersDataBase                      # importing users database module
from replies import msgProc                             # importing message pricessing function
from vars import group_token, debug, sleep_timeout, admin_token     # importing variables of bot init
import time
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
# import socket, urllib3, requests                      # for exception codes


# vk_api variable
vkBotSession = vk_api.VkApi(token=group_token)
# send message to id
def sendMsg(id, msg, attachments = ''):
    vkBotSession.method('messages.send', { 'user_id': id, 'message': msg, 'random_id': 0, 'attachment': ','.join(attachments) })


def main():

    # log onto db
    usersDataBase.updateList()

    # bot is running flag
    isBotRunning = True

    while isBotRunning:

        # get api for connecting to my community
        vkBotSession = vk_api.VkApi(token=group_token)
        vkBotApi = vkBotSession.get_api()
        vkLongpoll = VkLongPoll(vkBotSession)
        vkUpload = VkUpload(vkBotSession)


        # start console message
        print('\n\n\nBot has been strted. Messages log:\n\n')

        # catch vk session errors
        try:

            # main loop
            for event in vkLongpoll.listen():

                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        
                        # get and convert message to lower case
                        userMsg = event.text.lower()
                        userVkId = event.user_id
                        
                        # search user in database
                        userData = usersDataBase.getUserData(userVkId)
                        # create new user if his data doesnt exist
                        if not userData:
                            print('NEW USER\n')
                            # get user name by vk id
                            response = vkBotApi.users.get(user_ids=userVkId)
                            name = [str(response[0]['first_name']), str(response[0]['last_name'])]
                            # save user data
                            userData = {
                                'name': name,
                                'admin': False,
                                'group': '',
                                'nick': name[0]
                            }
                            # save data in db
                            usersDataBase.add2List(userVkId, userData)
                            usersDataBase.dumbList()

                        # console log message
                        print(userData['firstname'], userData['secondname'], 'id=' + str(userVkId))
                        print(time.ctime())
                        print(userMsg)

                        # turning bot off condition (admins only)
                        if userMsg == 'стоп':
                            if userData['admin']:
                                sendMsg(userVkId, 'ok')
                                isBotRunning = False
                                break
                            else:
                                # send message to non admin user tryna stop da bot
                                attachments = []
                                attachments.append( 'photo-205950303_457239039' )
                                vkBotSession.method('messages.send',
                                    {
                                        'user_id': userVkId,
                                        'message': 'ты не админ, соси',
                                        'random_id': get_random_id(),
                                        'attachment': ','.join(attachments)
                                    })

                        # get reply message
                        if debug:
                            botReply = msgProc(userVkId, userMsg, vkBotSession, vkUpload)
                        else:
                            # catch msg processing error
                            try:
                                botReply = msgProc(userVkId, userMsg, vkBotSession, vkUpload)
                            except BaseException:
                                botReply = 'ты блять его убил нахуй\nты его захуярил'
                                file = open('error_msgs.txt','a', encoding='utf-8')
                                file.write('///   NEW ERROR   ///\nMSG: "' + userMsg + '"\nTIME: ' + time.ctime() + '\n\n\n')
                                file.close()

                        # send reply to user
                        if botReply:
                            sendMsg(userVkId, botReply)
                            print('\nAnswered')

                        print('\n\n')

                # bot should sleep 4 better performance such as u
                time.sleep(sleep_timeout)


        # if vk is gay then restart connection
        # errrs: socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout
        except BaseException:   # vashe poxui
           True


# running script
if __name__ == "__main__":
	main()
