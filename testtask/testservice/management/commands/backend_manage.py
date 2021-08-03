from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from testservice.models import Backend

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-name', '-n',
                            nargs='?',
                            type=str,
                            default='',
                            required=True,
                            help='The name of backend to manage')
        parser.add_argument('-switch', '-s',
                            nargs='?',
                            type=str,
                            default='on',
                            choices=['on', 'off'],
                            required=True,
                            help='Swith on|off the backend')


    def handle(self, **options):
        backend_name = options['name']
        switch = options['switch']
        try:
            backends = Backend.objects.filter(name=backend_name)
        except ObjectDoesNotExist as e:
            print(f'Backend with name={backend_name} not found!')
        else:
            for b in backends:
                b.enabled = switch == 'on'
                b.save()
                print(f'Backend {b.classname}(name={b.name}) switched {switch}')
