import json


class UsersDataBase:

    def __init__(self):
        self.userlist = {}
        self.updateList

    def updateList(self):
        try:
            with open("users.json", "r") as f:
                self.userlist = json.load(f)
        except json.decoder.JSONDecodeError:
            print('JSON IS BROKEN')

    def getUsersList(self):
        return self.userlist

    def dumbList(self):
        userslist_update_str = json.dumps(self.userlist, sort_keys=True, indent=4)
        print('\n\nDB JUST BEEN UPDATED\n')
        #print('\n\n---NEW DB STATE---\n\n', userslist_update_str, '\n\n\n\n')
        with open('users.json', 'w') as f:
            f.write(userslist_update_str)

    def add2List(self, id, userData):
        if str(id) in self.userlist:
            del self.userlist[str(id)]
        self.userlist[str(id)] = userData

    def getUserData(self, id):
        if str(id) in self.userlist:
            return self.userlist[str(id)]
        return False

    def findIdByName(self, name):
        for id in self.userlist:
            if self.userlist[id]['firstname'].lower() == name or self.userlist[id]['nick'].lower() == name:
                return id
        return False

    def findIdByField(self, key, value):
        for id in self.userlist:
            if self.userlist[id][key].lower() == value:
                return id
        return False

    def forceUpdate(self):
        self.dumbList()
        self.updateList()


usersDataBase = UsersDataBase()