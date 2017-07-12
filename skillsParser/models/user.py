from copy import copy
from sqlalchemy import text


class User(object):
    _data = {}
    def __init__(self, raw):
        self._date = raw.get('Timestamp')
        self._email = raw.get('Email Address')
        self._discord = raw.get('Discord Username (optional)')
        self._data = copy(raw)
        self._id = raw.get('id', None)
        self._previous_experience = raw.get('have you helped us before?', False)
        self._availability = raw.get('How much time can you dedicate to helping out?', '')
        self._skills = raw.get('What is your experience with what you selected above?', None)
        self._coder = raw.get('Would you be interested in coding for us?', 'No') == 'Yes'
        self._help_with = raw.get('What would you like to help with?', '')

        self.translation_map = {'N/A': 0, 'Beginner (1-2)': 1, 'Intermediate (3-5)': 3, 'Advanced':4, 'I am a GOD!': 5}

        self.languages= {}
        if self.coder:
            self.languages['Java'] = raw.get('Java')
            self.languages['PHP'] = raw.get('PHP')
            self.languages['Perl'] = raw.get('Perl')
            self.languages['Python'] = raw.get('Python')
            self.languages['Ruby'] = raw.get('Ruby')
            self.languages['HTML/JavaScript/CSS'] = raw.get('HTML/JavaScript/CSS')
            self.languages['Architectural Design'] = raw.get('Architectural Design')
            self.languages['API Design'] = raw.get('API Design')
            self.languages['UI Development'] = raw.get('UI Development')

    @property
    def email(self):
        return self._email

    @property
    def availability(self):
        return self._availability

    @property
    def coder(self):
        return self._coder

    @property
    def skills(self):
        return self._skills

    @property
    def previous_expr(self):
        return self._previous_experience

    @property
    def email(self):
        return self._email

    @property
    def date(self):
        return self._date

    @property
    def discord(self):
        return self._discord


    def __create_user(self, engine):
        query = text("""INSERT into skills.users (user_email, creation_date, discord, skills_details, availability, coder, previous_experience) VALUES
  (:email, :creation_date, :discord, :skills_details, :availability, :coder, :previous_experience ) """ )

        engine.execute(query,
                       creation_date=self.date,
                       email=self.email,
                       ## This is is far from perfect but it seems to work.
                       discord=unicode(self.discord),
                       availability=self.availability,
                       coder=self.coder,
                       skills_details=self.skills,
                       previous_experience=self.previous_expr)

        return self.email


    def __create_user_languages(self, engine, user_email):
        if not self.coder:
            return

        for lang in self.languages:
            skill = self.languages[lang]
            if skill is None:
                continue

            query = text("""INSERT into skills.user_programming_languages (user_email, user_language, skillset, description) 
                        VALUES (:user_email,  :language, :skillset, :description) """)
            engine.execute(query,
                           user_email=user_email,
                           language=lang.strip(),
                           skillset=self.translation_map.get(skill, 0),
                           description=skill)


    def __create_user_categories(self, cursor, user_email, categories):
        for c in categories:
            query = text("""INSERT into skills.user_categories (user_email, user_category) VALUES (:user_email, :category) """ )
            cursor.execute(query, user_email=user_email, category=c.strip())


    def persist(self, engine):
           user_email = self.__create_user(engine)
           print('created user: {}'.format(user_email))
           help = self._help_with
           items = self._help_with.split(',')
           if(len(items)) > 0:
                self.__create_user_categories(engine, user_email, items)

           self.__create_user_languages(engine, user_email)


