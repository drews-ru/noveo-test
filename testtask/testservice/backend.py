import json
from .models import Notification, Backend

class GenericBackend():
    """ Generic backend interface """
    model = Backend
    connected = False

    def __init__(self, name, parameters='{}', enabled=True):
        if name == '':
            raise ValueError('Backend name must not be empty')

        if self.is_valid_json(parameters):
            self.instance, created = self.model.objects.get_or_create(name=name)
            if created:
                self.instance.enabled=enabled
                self.instance.parameters=parameters
                self.instance.save()
            self.parameters = json.loads(self.instance.parameters)
        else:
            raise ValueError('Invalid JSON specified as backend parameters')


    def is_valid_json(self, parameters):
        """ Method for validation JSON backend parameters """
        try:
            json.loads(parameters)
        except:
            return False
        else:
            return True


    def is_valid(self, parameters):
        """ Method for basic validation backend parameters """
        pass


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




class EmailBackend(GenericBackend):
    """ Email backend interface """

    def send(self, message):
        super().send(message)


