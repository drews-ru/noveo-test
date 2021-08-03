from django.core.management.base import BaseCommand
from testservice.backend import *

class Command(BaseCommand):
    def handle(self, **options):
        print('List of all available backend types:')
        print('='*50)
        print([cls.__name__ for cls in GenericBackendInterface.__subclasses__()])
