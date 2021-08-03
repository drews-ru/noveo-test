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
                            help='The id of the backend to delete')

    def handle(self, **options):
        try:
            b = Backend.objects.get(id=options['id'])
        except Exception as e:
            print(e)
        else:
            print(f'You are going to delete backend [{b.id}] {b.classname}(name={b.name}, enabled={b.enabled})')
            answer = input('Are you shure? [yes/no]: ')
            if answer.lower() == 'y' or answer.lower() == 'yes':
                try:
                    b.delete()
                except Exception as e:
                    print(e)
                else:
                    print('Backend deleted successfully!')
                    call_command('backend_list')