from copy import copy
from sqlalchemy import text




class SkillModel(object):
    _data = {}

    known_categories = [
        "Any other assorted community/discord/whatever related tasks",
        "Chat/Forum Moderation",
        "Community Outreach (in person, or online social media)",
        # "Geeky Tour Guide (you'll see ^_~) https://goo.gl/t8Xhb5",
        "Geeky Tour Guide (you'll see ^_~)",
        'Animation',
        'Application development.',
        'Business Development',
        'Code/Sys Admin',
        'Content contribution',
        'Graphic Asset Creation',
        'Graphic Design',
        'Marketing',
        'Music Creation',
        'Project Managment',
        'Public Relations',
        'Researching all the things',
        'Server and data infrastructure',
        'Video Creation',
        'Video Editing',
        'Video Editing, Video Creation',
        'Web Design',
        'Web Development',
        'Writing'
    ]

    def __init__(self, raw):


        self._date = raw.get('Timestamp')
        self._email = raw.get('Email Address')
        self._discord = raw.get('Discord Username (optional)')
        self._data = copy(raw)
        self._id = raw.get('id', None)
        self._previous_experience = raw.get('Have you helped us before?')
        self._availability = raw.get('How much time can you dedicate to helping out?', '')
        self._skills = raw.get('What is your experience with what you selected above?', None)
        self._coder = raw.get('Would you be interested in coding for us?', 'No') == 'Yes'
        self._help_with = raw.get('What would you like to help with?', '')
        # self._other = None

        self.translation_map = {'N/A': 0, 'Beginner (1-2)': 1, 'Intermediate (3-5)': 3, 'Advanced': 4, 'I am a GOD!': 5}

        self.languages = {}
        if self.coder:
            self.languages['Java'] = raw.get('Java')
            self.languages['PHP'] = raw.get('PHP')
            self.languages['Perl'] = raw.get('Perl')
            self.languages['Python'] = raw.get('Python')
            self.languages['Ruby'] = raw.get('Ruby')
            self.languages['HTML/JavaScript/CSS'] = raw.get('HTML/JavaScript/CSS')

        self._arch_design = raw.get('Architectural Design')
        self._api_design = raw.get('API Design', '')
        self._ui_development = raw.get('UI Development', '')

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
    def date(self):
        return self._date

    @property
    def discord(self):
        return self._discord

    def __create_user(self, engine):
        # Create the baseline user if he doesn't exist.
        create_user_query = text("""INSERT into global_data.users (user_email, creation_date, discord) VALUES
  (:email, :creation_date, :discord ) ON CONFLICT do NOTHING """)
        engine.execute(create_user_query,
                       creation_date=self.date,
                       email=self.email,
                       discord=str(self.discord))

        query = text("""INSERT into skills.user_skills_metadata (user_email, creation_date, skills_details, 
                        availability, coder, previous_experience, architectual_design, api_design, ui_development, help_with) VALUES
  (:email, :creation_date, :skills_details, :availability, :coder, :previous_experience, :architech, :api, :ui_devel, :help_with) 
            ON CONFLICT(user_email) do UPDATE
            SET skills_details =:skills_details,
                availability = :availability,
                coder = :coder,
                previous_experience = :previous_experience,
                architectual_design = :architech,
                api_design = :api,
                ui_development = :ui_devel,
                help_with = :help_with
                """)

        engine.execute(query,
                       creation_date=self.date,
                       email=self.email,
                       # This is is far from perfect but it seems to work.
                       availability=self.availability,
                       coder=self.coder,
                       skills_details=self.skills,
                       previous_experience=self.previous_expr,
                       architech=self._arch_design,
                       api=self._api_design,
                       ui_devel = self._ui_development,
                       help_with = self._help_with

                       )

        return self.email

    def __create_user_languages(self, engine, user_email):
        if not self.coder:
            return

        for lang in self.languages:
            skill = self.languages[lang]
            if skill is None:
                continue

            # Delete old data.
            query = text("""DELETE FROM skills.user_programming_languages where user_email=:user_email""")
            engine.execute(query, user_email=user_email)

            query = text("""INSERT into skills.user_programming_languages (user_email, user_language, skillset, description) 
                        VALUES (:user_email,  :language, :skillset, :description) 
                        ON CONFLICT DO NOTHING """)
            engine.execute(query,
                           user_email=user_email,
                           language=lang.strip(),
                           skillset=self.translation_map.get(skill, 0),
                           description=skill)

    def __create_user_categories(self, engine, user_email):
        query = text("""DELETE FROM skills.user_categories where user_email=:user_email""")
        engine.execute(query, user_email=user_email)
        for category  in self.known_categories:
            if category not in self._help_with:
                continue
            query = text("""INSERT into skills.user_categories (user_email, user_category) VALUES (:user_email, :category) 
                            ON CONFLICT DO NOTHING """)
            engine.execute(query, user_email=user_email, category=category.strip())

    def persist(self, engine):
        if (self.email is None):
            return
        # items = []
        # for f in self._help_with.split(','):
        #     items.append(f.strip())

        self._other =  self._help_with
        user_email = self.__create_user(engine)
        print('created user: {}'.format(user_email))
        if (len(self._help_with)) > 0:
            self.__create_user_categories(engine, user_email)

        self.__create_user_languages(engine, user_email)
