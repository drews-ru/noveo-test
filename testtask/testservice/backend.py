import json
import logging
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, ValidationError, EmailStr, SecretStr, constr
from enum import Enum
from .models import Backend


def instantiate_backend(classname, *args, **kwargs):
    constructor = globals()[classname]
    return constructor(*args, **kwargs)


class GenericBackendInterface():
    """ Generic backend interface """
    model = Backend
    connected = False

    class Settings(BaseModel):
        """ Empty settings for the generic backend interface """
        pass


    def __init__(self, name, settings='{}', enabled=True):
        if name == '':
            raise ValueError('Backend name must not be empty')

        if not self.is_valid_json(settings):
            raise ValueError('Invalid JSON specified as backend settings')

        if not self.is_valid(settings):
            self.help()
            raise ValueError('Settings are not valid for this backend. See backend help.')

        self.instance, created = \
            self.model.objects.get_or_create(name=name,
                                             classname=self.__class__.__name__)
        if created:
            self.instance.enabled=enabled
            self.instance.settings=settings
            self.instance.save()

        self.settings = self.Settings(**json.loads(self.instance.settings))


    def help(self):
        """ Output backend settings description """
        print('This is a generic backend interface, so it has no settings')


    def is_valid_json(self, settings):
        """ Method for validation JSON backend settings """
        try:
            json.loads(settings)
        except:
            return False
        else:
            return True


    def is_valid(self, settings):
        """ Method for validation generic backend settings """
        try:
            s = self.Settings(**json.loads(settings))
        except ValidationError as e:
            print(e)
            return False
        else:
            self.settings = s
            return True


    def enable(self):
        """ Method to enable backend """
        self.instance.enabled = True
        self.instance.save()


    def disable(self):
        """ Method to disable backend """
        self.instance.enabled = False
        self.instance.save()


    def is_enabled(self):
        """ Method to check if backend enabled or not """
        self.instance.refresh_from_db()
        return self.instance.enabled


    def connect(self):
        """ Method to connect with backend (should be overridden if necessary) """
        # Making specific connection routine for the specific backend
        self.connected = True


    def send(self, message):
        """ Method for sending message to backend """
        if self.instance.enabled and message:
            if not self.connected:
                self.connect()
            return {'backend': self.__class__.__name__, 'sent': True}
        else:
            return {'backend': self.__class__.__name__, 'sent': False}



class EmailBackendInterface(GenericBackendInterface):
    """ Email backend interface (not completed) """

    class Settings(BaseModel):
        address: EmailStr
        user: str
        password: SecretStr
        subject: Optional[str]

    def __init__(self, *args, **kwargs):
        super(EmailBackendInterface, self).__init__(*args, **kwargs)
        if not self.settings.subject:
            self.settings.subject = f'Notification email from {self.__class__.__name__}'


    def help(self):
        print('Settings for the email backend: address [required]')

    def send(self, message):
        result = super(EmailBackendInterface, self).send(message)

        """ Here should be code for sending email """

        return result


class TelegrambotBackendInterface(GenericBackendInterface):
    """ Telegram bot backend interface (working) """
    bot = None

    class Settings(BaseModel):
        token: SecretStr
        channel: constr(regex=r'^@')

    def __init__(self, *args, **kwargs):
        super(TelegrambotBackendInterface, self).__init__(*args, **kwargs)
        import telebot
        try:
            self.bot = telebot.TeleBot(self.settings.token.get_secret_value())
        except:
            self.connected = False
        else:
            self.connected = True

    def help(self):
        print('Settings for the telegram bot backend: token [required], channel [required, starts with "@"]')

    def connect(self):
        if not self.bot:
            self.connected = False

    def send(self, message):
        result = super(TelegrambotBackendInterface, self).send(message)
        if self.connected and result['sent']:
            self.bot.send_message(self.settings.channel, message)
        return result




class LogLevelEnum(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'

class LogBackendInterface(GenericBackendInterface):
    """ Log backend interface (working) """
    global loggers

    class Settings(BaseModel):
        filename: Path
        format: Optional[str]
        loglevel: LogLevelEnum = LogLevelEnum.INFO

    def __init__(self, *args, **kwargs):
        super(LogBackendInterface, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.instance.name)
        self.logger.setLevel(getattr(logging, self.settings.loglevel.upper()))
        file_handler = logging.FileHandler(self.settings.filename, encoding='utf-8')

        if self.settings.format:
            formatter = logging.Formatter(self.settings.format)
            file_handler.setFormatter(formatter)

        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        self.logger.addHandler(file_handler)


    def help(self):
        print('Settings for the log backend: filename [required], format [optional], loglevel [optional]')


    def send(self, message):
        result = super(LogBackendInterface, self).send(message)

        try:
            if result['sent']:
                getattr(self.logger, self.settings.loglevel.value)(message)
        except:
            result['sent'] = False
        finally:
            return result