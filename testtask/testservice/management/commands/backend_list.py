from django.core.management.base import BaseCommand
from testservice.models import Backend

class Command(BaseCommand):
    def handle(self, **options):
        print('List of the registered backends:')
        print('='*50)
        backends = Backend.objects.all()
        for b in backends:
            print(f'[{b.id}] {b.classname}(name={b.name}, enabled={b.enabled})')