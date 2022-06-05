from random import randint
from vk_api import bot_longpoll
from users_db import usersDataBase                          # importing users database module
from server_global_settings import globalServerSettings
from replies import msgProc, sendEmail2Admin, sendMsg2id, sendMsgWithPhoto    # importing message pricessing function
from vars import group_token, debug, sleep_timeout, admin_token, dbUpdateCooldown, admin_id, public_id     # importing variables of bot init
import time
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import CHAT_START_ID, VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
# import socket, urllib3, requests                      # for exception codes
import linecache
import sys


# vk_api variable
vkBotSession = vk_api.VkApi(token=group_token)
# send message to id
def sendMsg(id, msg, attachments = ''):
    vkBotSession.get_api().messages.send(peer_id=id, message=msg, random_id = 0)
    #vkBotSession.method('messages.send', { 'user_id': id, 'message': msg, 'random_id': 0, 'attachment': ','.join(attachments) })


def TextException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"):\n{}'.format(filename, lineno, line.strip(), exc_obj)


def main():

    # log onto db
    usersDataBase.updateList()
    globalServerSettings.update()

    # bot is running flag
    isBotRunning = True

    # db update timer
    dbTimer = time.time()

    while isBotRunning:

        # get api for connecting to my community
        vkBotSession = vk_api.VkApi(token=group_token)
        vkBotApi = vkBotSession.get_api()
        vkLongpoll = VkBotLongPoll(vkBotSession, public_id)
        vkUpload = VkUpload(vkBotSession)


        # start console message
        print('\n\n\nBot has been strted. Messages log:\n\n')

        # catch vk session errors
        try:

            # main loop
            for event in vkLongpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW and ( event.from_chat or event.from_user ):

                        # print(event)
                        
                        # get message
                        userMsg = event.message.text
                        userVkId = event.message.from_id
                        chatId = False
                        if event.from_chat:
                            chatId = event.chat_id + bot_longpoll.CHAT_START_ID
                        fwdMsgs = []
                        for msg in event.message.fwd_messages:
                            fwdMsgs.append(msg['text'])

                        # if new user in chat
                        if chatId and 'action' in event.message:
                            if event.message['action']['type'] == 'chat_invite_user':
                                memberId = str(event.message['action']['member_id'])
                                name = vkBotApi.users.get(user_ids=memberId)[0]['first_name']
                                sendMsgWithPhoto(vkBotSession, chatId, 'Добро пожаловать, @id' + memberId + ' (' + name + ')', 
                                    'https://sun9-55.userapi.com/impg/q1LpyI9Ee5nljJbs7bVH9PM_HtRdnUmCamsC0A/azoIGKs0u4I.jpg?size=640x640&quality=96&sign=4207452937cb3598f54553226670d002&type=album',
                                    vkUpload)
                                continue
                        
                        # search user in database
                        userData = usersDataBase.getUserData(userVkId)
                        # create new user if his data doesnt exist
                        if not userData:
                            print('NEW USER\n')
                            # get user name by vk id
                            userData = {}
                            if userVkId > 0 and userVkId < CHAT_START_ID:
                                response = vkBotApi.users.get(user_ids=userVkId, fields='sex')[0]
                                man = True
                                if response['sex'] == 1:
                                    man = False
                                userData = {
                                    'firstname': str(response['first_name']),
                                    'secondname': str(response['last_name']),
                                    'admin': 6,
                                    'group': '',
                                    'nick': str(response['first_name']),
                                    'msgCount': 0,
                                    'man': man
                                }
                            else:
                                userData = {
                                    'firstname': 'bot',
                                    'secondname': str(randint(0, 1000)),
                                    'admin': 5,
                                    'msgCount': 0,
                                }
                            # save data in db
                            usersDataBase.add2List(userVkId, userData)
                            usersDataBase.forceUpdate()

                        # console log message
                        print(userData['firstname'], userData['secondname'], 'id=' + str(userVkId))
                        print(time.ctime())
                        print(userMsg)
                        if fwdMsgs:
                            print('forward msgs:\n', fwdMsgs)

                        # turning bot off condition (admins 500 only)
                        if userMsg == 'стоп' or userMsg == 'stop':
                            if userData['admin'] >= 500:
                                sendMsg(userVkId, 'ok')
                                sendMsg2id(vkBotSession, admin_id, '@id' + str(userVkId) + ' ВЫКЛЮЧИЛ БОТА')
                                usersDataBase.forceUpdate()
                                globalServerSettings.forceUpdate()
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
                            botReply = msgProc(userVkId, userMsg, vkBotSession, vkUpload, fwdMsgs, chatId)
                        else:
                            # catch msg processing error
                            try:
                                botReply = msgProc(userVkId, userMsg, vkBotSession, vkUpload, fwdMsgs, chatId)
                            except BaseException:
                                botReply = 'ваши действия привели к ошибке и bот умер :С\nно его воскресили C:'
                                err = TextException()
                                print(err)
                                file = open('error_msgs.txt','a', encoding='utf-8')
                                file.write('///   NEW ERROR   ///\nMSG: "' + userMsg + '\nERR: "' + err + '"\nTIME: ' + time.ctime() + '\n\n\n')
                                file.close()

                        # send reply
                        if botReply:
                            # update user messages counter
                            userData['msgCount'] += 1
                            if botReply != -1:
                                # send reply (to chat or to user)
                                if chatId:
                                    sendMsg(chatId, botReply)
                                else:
                                    sendMsg(userVkId, botReply)
                            print('\nAnswered')

                        print('\n\n')


                # update db
                if (time.time() - dbTimer) >= dbUpdateCooldown:
                    usersDataBase.forceUpdate()
                    globalServerSettings.forceUpdate()
                    dbTimer = time.time()


                # bot should sleep 4 better performance such as u
                # time.sleep(sleep_timeout)


        # if vk is gay then restart connection
        # errrs: socket.timeout, urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout
        except BaseException as err_msg:   # vashe poxui
            if debug:
                print(err_msg)
                isBotRunning = False
            else:
                print('\n\nBOT HAS BEEN RESTARTED\n\n')
                file = open('error_msgs.txt','a', encoding='utf-8')
                file.write('///   NEW ERROR   ///\n' + '\nERR: ' + str(err_msg) + '\nTIME: ' + time.ctime() + '\n\n\n')
                file.close()



# running script
if __name__ == "__main__":
	main()
