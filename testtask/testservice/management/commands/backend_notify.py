import json
from django.core.management.base import BaseCommand
from testservice.serializers import NotificationSerializer
from testservice.backend import *

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-message', '-m',
                            nargs='?',
                            type=str,
                            default='{"message": "Testservice started up successfully!", "sender": "Testservice", "sender_ip": "localhost"}',
                            required=False,
                            help='Default startup notification')

    def handle(self, **options):
        serializer = NotificationSerializer(data=json.loads(options['message']))
        if serializer.is_valid():
            notification = serializer.save()

            for item in Backend.objects.filter(enabled=True):
                instance = instantiate_backend(item.classname, item.name, settings=item.settings)
                try:
                    result = instance.send(notification.message)
                except Exception as e:
                    print(e)
                else:
                    print(f'Sending to [{item.id}] {item.classname}(name={item.name}) : message({notification.message}) -> ok')

