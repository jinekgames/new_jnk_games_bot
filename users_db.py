import json


class UsersDataBase:

    def __init__(self):
        self.userlist = {}
        self.updateList

    def updateList(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                self.userlist = json.load(f)
        except json.decoder.JSONDecodeError:
            print('JSON IS BROKEN')

    def getUsersList(self):
        return self.userlist

    def dumbList(self):
        userslist_update_str = json.dumps(self.userlist, sort_keys=False, indent=4, ensure_ascii=True, separators=(',', ': '))
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

    def findIdByFieldS(self, keylist, valuelist):
        len_key = len(keylist)
        len_val = len(valuelist)
        if len_key != len_val:
            return 'error blyat vy dolbaeb'
        for id in self.userlist:
            i = 0
            while i < len_key:
                if self.userlist[id][keylist[i]].lower().replace('ё', 'е') != valuelist[i].replace('ё', 'е'):
                    break
                i += 1
            if i == len_key:
                return id
        return False

    def forceUpdate(self):
        self.dumbList()
        self.updateList()

    def getSortedList(self, keys, sortBy, reverse = False):
        if not sortBy in keys:
            return 'error blyat vy dolbaeb'
        resList = []
        for id in self.userlist:
            listEl = {}
            flag = False
            for key in keys:
                if not key in self.userlist[id]:
                    flag = True
                    break
            if flag:
                continue
            for key in keys:
                listEl[key] = self.userlist[id][key]
            listEl['id'] = id
            resList.append(listEl)
        resListLen = len(resList)
        if reverse:
            for i in range(resListLen):
                for k in range(i):
                    if resList[i][sortBy] > resList[k][sortBy]:
                        tmp = resList[i]
                        resList[i] = resList[k]
                        resList[k] = tmp
        else:
            for i in range(resListLen):
                for k in range(i):
                    if resList[i][sortBy] < resList[k][sortBy]:
                        tmp = resList[i]
                        resList[i] = resList[k]
                        resList[k] = tmp
        return resList

    def updateFieldByFooOfId(self, key, valueFoo):
        for id in self.userlist:
            if self.userlist[id]['firstname'] == 'bot':
                continue
            self.userlist[id][key] = valueFoo(id)



usersDataBase = UsersDataBase()
