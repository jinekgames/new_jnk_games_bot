import json


__JSON_NAME__ = 'server_global_settings.json'


class GlobalServerSettings:

    def __init__(self):
        self.settings = {}
        self.update

    def update(self):
        try:
            with open(__JSON_NAME__, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            return True
        except json.decoder.JSONDecodeError:
            print('JSON of server settings IS BROKEN')
            return False

    def get(self):
        return self.settings

    def dumb(self):
        try:
            userslist_update_str = json.dumps(self.settings, sort_keys=False, indent=4, ensure_ascii=True, separators=(',', ': '))
            print('\n\nDB JUST BEEN UPDATED\n')
            with open(__JSON_NAME__, 'w') as f:
                f.write(userslist_update_str)
                return True
        except BaseException:
            print('dumb server settings ERROR !!!!')
            return False

    def setSetting(self, key, str_value):
        if str(key) in self.settings:
            del self.settings[str(key)]
        self.settings[str(key)] = str_value
        self.forceUpdate()

    def getSetting(self, key):
        if str(key) in self.settings:
            return self.settings[str(key)]
        return False

    def forceUpdate(self):
        self.dumb()
        self.update()



globalServerSettings = GlobalServerSettings()
