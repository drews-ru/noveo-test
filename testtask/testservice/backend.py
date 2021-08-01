import json
import logging
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, ValidationError, EmailStr, FilePath
from .models import Notification, Backend


def instatiate_backend(classname, *args, **kwargs):
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
        print('This is a generic backend interface, so has no settings')


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
        """ Method to connect with backend (should be overridden) """
        # Making specific connection routine for the specific backend
        self.connected = True


    def send(self, message):
        """ Method for sending message to backend (should be overridden) """
        if not self.connected:
            self.connect()


class EmailBackendInterface(GenericBackendInterface):
    """ Email backend interface """

    class Settings(BaseModel):
        address: EmailStr

    def send(self, message):
        super(EmailBackendInterface, self).send(message)


class LogBackendInterface(GenericBackendInterface):
    """ Log backend interface """

    class Settings(BaseModel):
        filename: Path
        format: Optional[str]

    def __init__(self, *args, **kwargs):
        super(LogBackendInterface, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.instance.name)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(self.settings.filename, encoding='utf-8')

        if self.settings.format:
            formatter = logging.Formatter(self.settings.format)
            file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def help(self):
        print('Settings for the log backend: filename [required]')


    def send(self, message):
        self.logger.info(message)
