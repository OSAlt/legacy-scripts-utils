import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from abc import ABCMeta, abstractmethod


class BaseParser(metaclass=ABCMeta):
    def __init__(self, config_file):
        self.db_config = None
        f = open(config_file)
        data = yaml.load(f)
        f.close()
        self.config = data
        self.debug = self.config.get('debug', False)

    def __construct_dsn__(self):
        """
        generates a dsn connection string based on the yaml configuration.
        :return: string representation
        """
        db_settings = self.config['database']
        self.dsn = 'dbname={database} host={host} port={port} user={user} password={password}' \
            .format(**db_settings).replace('$HOSTNAME', db_settings['host'])

        self.db_config = {
            'drivername': db_settings.get('engine', 'mysql+pymysql'),
            'host': db_settings['host'],
            'port': db_settings['port'],
            'username': db_settings['user'],
            'password': db_settings['password'],
            'database': db_settings['database'],
            'schema': db_settings['schema']

        }
        self.connection_string = "{engine}://{user}:{password}@{host}:{port}/{database}".format(**db_settings)

    def get_alchemy_connection(self):
        """
         Uses the DB settings to create a sqlalchemy engine + session.
        :return:
        """
        if self.db_config is None:
            self.__construct_dsn__()

        echo_sql = True if self.debug else False
        engine = create_engine(self.connection_string, echo=echo_sql, encoding=self.db_config.get('encoding', 'utf8'))
        session = sessionmaker(bind=engine)
        return (engine, session)

    @abstractmethod
    def read_sheet(self):
        pass


    @abstractmethod
    def run(self):
        pass



