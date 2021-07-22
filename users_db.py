import json

"""

open json users list
with open("users.json", "r") as f:
userslist = json.load(f)

"""


class DataBase:

    def __init__(self):
        self.userlist = {}

    def updateList(self):
        try:
            with open("users.json", "r") as f:
                self.userlist = json.load(f)
        except json.decoder.JSONDecodeError:
            print('JSON IS BROKEN')

    def usersList(self):
        return self.userlist

    def dumbList(self):
        userslist_update_str = json.dumps(self.userlist, sort_keys=True, indent=4)
        print('\n\n', userslist_update_str, '\n\n\n\n')
        with open('users.json', 'w') as f:
            f.write(userslist_update_str)

    def add2List(self, id, userData):
        if str(id) in self.userlist:
            del self.userlist[str(id)]
        self.userlist[str(id)] = userData
        self.dumbList()
        self.updateList()

    def getUserData(self, id):
        if str(id) in self.userlist:
            return self.userlist[str(id)]
        return False

    def findIdByName(self, name):
        for id in self.userlist:
            print('\n', self.userlist[id], '\n')
            if self.userlist[id]['name'][0].lower() == name or self.userlist[id]['nick'].lower() == name:
                return id

        # name = transliterate.translit(name, 'ru', reversed=True)
        # print(name)

        return False
