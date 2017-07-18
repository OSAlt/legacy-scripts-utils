from copy import copy
from sqlalchemy import text


class User(object):
    _data = {}

    def __init__(self, raw):
        self._date = raw.get('Timestamp')
        self._email = raw.get('Email Address')
        self._discord = raw.get('Discord Username (preferred)')
        self._data = copy(raw)
        self._camera_friendly = raw.get('Are you comfortable with speaking and interacting on camera?', 'No') == 'Yes'
        self._guide = raw.get('Are you willing to be our guide if we visit your area?', 'No') == 'Yes'
        self._host = raw.get('Can we stay with you? (Must be able host at least two people)', 'No') == 'Yes'
        self._transport = raw.get('Do you have the ability to transport us around? (Minimum of two passengers)',
                                  'No') == 'Yes'
        self._speak_local_dialect = raw.get(
            'In addition to English, can you speak the language of the country you are in?', 'No') == 'Yes'
        self._geeky_venues = raw.get(
            'What are all the Geeky places/gatherings in your area?  Give us all the details =)', '')
        self._city = raw.get('What is your nearest major city?', '')
        self._country = raw.get('Which country to do you live in?', '')

    @property
    def email(self):
        return self._email

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
        ## Create the baseline user if he doesn't exist.
        create_user_query = text("""INSERT into global_data.users (user_email, creation_date, discord) VALUES
  (:email, :creation_date, :discord ) ON CONFLICT do NOTHING """)
        engine.execute(create_user_query,
                       creation_date=self.date,
                       email=self.email,
                       discord=unicode(self.discord))

        query = text("""INSERT into geeksabroad.user_abroad_metadata (user_email, creation_date,  country, major_city, 
                        geeky_events_nearby, guide, fluent_local_dialect, camera_friendly, provides_transport, 
                        provides_lodging) VALUES (:email, :creation_date, :country, :city, :geek_events, :guide,
                        :fluent, :camera_friendly, :transport, :lodging) 
            ON CONFLICT(user_email) do UPDATE SET 
           country=:country, 
           major_city=:city, 
           geeky_events_nearby=:geek_events, 
           guide=:guide, 
           fluent_local_dialect=:fluent, 
           camera_friendly=:camera_friendly, 
           provides_transport=:transport, 
           provides_lodging=:lodging """)

        engine.execute(query,
                       creation_date=self.date,
                       email=self.email,
                       country=self._country,
                       city=self._city,
                       geek_events=self._geeky_venues,
                       guide=self._guide,
                       fluent=self._speak_local_dialect,
                       camera_friendly=self._camera_friendly,
                       transport=self._transport,
                       lodging=self._host)
        ## This is is far from perfect but it seems to work.

        return self.email

    def persist(self, engine):
        if(self.email is None):
            return
        user_email = self.__create_user(engine)
        print('created user: {} for geeks abroad'.format(user_email))
