

class User(object):
    _data = {}
    def __init__(self, raw):
        self._date = raw.get('Timestamp')
        self._email = raw.get('Email Address')
        self._discord = raw.get('Discord Username (optional)')

    @property
    def email(self):
        return self._email

    @property
    def date(self):
        return self._date

    @property
    def discord(self):
        return self._date

