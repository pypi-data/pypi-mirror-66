# http://stackoverflow.com/questions/13789235/how-to-initialize-singleton-derived-object-once
# https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
import getpass
import json
import os
import platform
from pprint import pprint
from os.path import expanduser


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self, *args, **kwargs):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated(*args, **kwargs)
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

class Config():

    PLATFORM = platform.system()
    USERNAME_OS = getpass.getuser()

    def __init__(s):

        if not hasattr(s, 'ROOT_DIR'):
            raise Exception('Must define ROOT_DIR first')

        ROOT_DIR = s.ROOT_DIR
        s.config = s.load_config()
        s._ENV = s.config.get('env')

        s.USE_SQLITE = s.config.get('use_sqlite', False) # Support SQLite and MySQL only, so True for SQLite, False for MySQL
        s.DATABASE_NAME = s.config.get('database', False)

        s.APP_PATH = ROOT_DIR + '/app'
        s.BIN_PATH = ROOT_DIR + '/app/bin'
        s.DIST_PATH = ROOT_DIR + '/dist'
        s.PICKLE_PATH = ROOT_DIR + '/dist/pickle'
        s.LOG_PATH = s.DIST_PATH + '/log'

        s.CONFIG_PATH = ROOT_DIR + '/dist/config'
        s.EXCEL_PATH = ROOT_DIR + '/dist/_excel'

        # Custom this direct, because it really large file.
        s.HTML_PATH = s.config.get('html_path', s.DIST_PATH + '/_html')
        s.IMAGES_PATH = s.config.get('images_path', s.DIST_PATH + '/_image')
        s.DATABASE_PATH = s.config.get('database_path', s.DIST_PATH + '/config/database')
        s.USER_PATH = s.config.get('user_path', str(expanduser("~")))

        s.GOOGLE_SHEET_CREDENTIALS = s.config.get('google_sheet_credentials', '')
        s.GOOGLE_SHEET_TOKENS = s.config.get('google_sheet_tokens', '')

        s.USER_DESKTOP = s.USER_PATH + '/Desktop'
        s.DOCUMENTS_PATH = s.USER_PATH + '/Documents'

        BIN_PATH = s.BIN_PATH

        s.CHROME_EXECUTABLE_PATH = BIN_PATH + '/chromedriver.exe'
        s.FIREFOX_EXECUTABLE_PATH = BIN_PATH + '/geckodriver.exe'
        s.FIREFOX_32_EXECUTABLE_PATH = BIN_PATH + '/geckodriver32.exe'
        s.PHANTOMJS_EXECUTABLE_PATH = BIN_PATH + '/phantomjs.exe'

        s.MAC_CHROME_EXECUTABLE_PATH = BIN_PATH + '/chromedriver'
        s.MAC_FIREFOX_EXECUTABLE_PATH = BIN_PATH + '/geckodriver'
        s.MAC_PHANTOMJS_EXECUTABLE_PATH = BIN_PATH + '/phantomjs'

        # s.LINUX_CHROME_EXECUTABLE_PATH = BIN_PATH + '/linux_chromedriver'
        # s.LINUX_FIREFOX_EXECUTABLE_PATH = BIN_PATH + '/linux_geckodriver'
        # s.LINUX_PHANTOMJS_EXECUTABLE_PATH = BIN_PATH + '/linux_phantomjs'

        if s.config.get('use_mongo_db', False):
            from mongoengine import connect
            connect(s.DATABASE_NAME, host=s.config.get('mongodb').get('host'))

    def reconnect_mongodb(self, database):
        from mongoengine import connect, disconnect
        disconnect()
        connect(database, host=self.config.get('mongodb').get('host'))

    def load_config(self):
        file = self.ROOT_DIR + '/config.json'
        if not os.path.exists(file):
            from swissarmykit.templates.config_default import ConfigDefault
            ConfigDefault.generate_config(file)

        d = json.loads(open(file, "r").read())
        return {**d.get('default'), **d.get(os.environ.get('AI_ENV', 'dev'))} # dev, prod


    def get_images_path(self):
        return self.IMAGES_PATH

    def get_html_path(self):
        return self.HTML_PATH

    def get_desktop_path(self):
        return self.USER_DESKTOP

    @staticmethod
    def is_win():
        return Config.PLATFORM == 'Windows'

    @staticmethod
    def is_win_32():
        return Config.PLATFORM == 'x86'

    @staticmethod
    def is_mac():
        return Config.PLATFORM == 'Darwin'

    def get_config(self, name=None):
        if not name:
            return self.config

        if '.' in name:
            c = self.config
            for n_ in name.split('.'):
                c = c[n_]
            return c.value

        return self.config[name]

    def init_folder(self):
        for folder in [
            self.DIST_PATH,
            self.PICKLE_PATH,
            self.LOG_PATH,

            self.EXCEL_PATH,
            self.CONFIG_PATH,
            self.HTML_PATH,
            self.IMAGES_PATH,
            self.DATABASE_PATH,
        ]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print('INFO: Create success dir ', folder)

    def is_use_mysql(self):
        return not self.USE_SQLITE

    def create_path_if_not_exist(self, file_path):
        ''' Ref: https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist'''
        path = os.path.dirname(file_path)
        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)
            return False

    def show_data(self):
        pprint(vars(self))

    def __repr__(self):
        # Because Ipython always print this
        try:
            import __main__ as main
            if hasattr(main, '__file__'):
                pprint(vars(self))
        except Exception as e:
            print(e)
        return ''

if __name__ == '__main__':
    print(os.environ.get('AI_ENV', 'dev'))
