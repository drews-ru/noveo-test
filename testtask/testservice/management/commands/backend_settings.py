import json
from django.core.management import call_command
from django.core.management.base import BaseCommand
from testservice.models import Backend

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-id', '-i',
                            nargs='?',
                            type=int,
                            default=0,
                            required=True,
                            help='The id of the backend which settings to show')

    def handle(self, **options):
        try:
            b = Backend.objects.get(id=options['id'])
        except Exception as e:
            print(e)
        else:
            print(f'Backend [{b.id}] {b.classname}(name={b.name}) settings:')
            print('='*50)
            print(json.loads(b.settings))
