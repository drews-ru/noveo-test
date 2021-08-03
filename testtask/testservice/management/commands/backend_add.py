from django.core.management.base import BaseCommand
from testservice.backend import *

class Command(BaseCommand):

    backend_classes = [cls.__name__ for cls in GenericBackendInterface.__subclasses__()]

    def add_arguments(self, parser):
        parser.add_argument('-name', '-n',
                            nargs='?',
                            type=str,
                            default='',
                            required=True,
                            help='The name of backend to add')
        parser.add_argument('-type', '-t',
                            nargs='?',
                            type=str,
                            default=self.backend_classes[0],
                            choices=self.backend_classes,
                            required=True,
                            help=f'Type of the backend to add. Choose from: {self.backend_classes}')
        parser.add_argument('-settings', '-s',
                            nargs='?',
                            type=str,
                            default='{}',
                            required=True,
                            help='Settings JSON for the backend')


    def handle(self, **options):
        try:
            backend = instantiate_backend(options['type'],
                                           name=options['name'],
                                           settings=options['settings']).instance
        except Exception as e:
            print(e)
        else:
            print(f'Backend added or exists: [{backend.id}] {backend.classname}(name={backend.name})')