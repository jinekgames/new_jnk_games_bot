import json

# open json users list
# with open("users.json", "r") as f:
#     userslist = json.load(f)

class list:
    userlist = {}

def updateList():
    try:
        with open("users.json", "r") as f:
            list.userlist = json.load(f)
    except json.decoder.JSONDecodeError:
        print('JSON IS BROKEN')


def usersList():
    return list.userlist

def dumbList():
    userslist_update_str = json.dumps(list.userlist, sort_keys=True, indent=4)
    print('\n\n', userslist_update_str, '\n\n\n\n')
    with open('users.json', 'w') as f:
        f.write(userslist_update_str)

def add2List(id, userData):
    if str(id) in list.userlist:
        del list.userlist[str(id)]
    list.userlist[str(id)] = userData
    dumbList()
    updateList()

def getUserData(id):
    if str(id) in list.userlist:
        return list.userlist[str(id)]
    return False

def findIdByName(name):
    for id in list.userlist:
        print('\n', list.userlist[id], '\n')
        if list.userlist[id]['name'][0].lower() == name or list.userlist[id]['nick'].lower() == name:
            return id

    # name = transliterate.translit(name, 'ru', reversed=True)
    # print(name)

    return False