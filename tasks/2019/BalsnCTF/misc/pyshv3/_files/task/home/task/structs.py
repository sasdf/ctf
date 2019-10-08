class User(object):
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.isadmin = 0
        self.prompt = ''
