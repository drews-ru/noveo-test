from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification, Backend
from .serializers import NotificationSerializer
from .backend import instantiate_backend

import asyncio
from asgiref.sync import async_to_sync, sync_to_async

@async_to_sync
async def run_tasks(notification: NotificationSerializer):
    backends = await sync_to_async(get_backends)()
    loop = asyncio.get_event_loop()
    for backend in backends:
        task = loop.create_task(sync_to_async(backend.send)(notification))
        loop.create_task(task_complete(task))


async def task_complete(task: asyncio.Task):
    await asyncio.sleep(5)
    if task.done():
        print(f'Dispatcher task for {task.result()["backend"]} completed: sent={task.result()["sent"]}')
    else:
        print('Dispatcher task not completed after 5 seconds, aborting')
        task.cancel()


#@sync_to_async
@api_view(['POST'])
def listener(request):
    """
    Service listening incoming messages to dispatch notifications to the registered backends
    """
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        if ip:
            request.data['sender_ip'] = ip
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # Running background tasks
            run_tasks(serializer.data['message'])

            return Response(instance.id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_backends():
    backends = []
    for item in Backend.objects.filter(enabled=True):
        instance = instantiate_backend(item.classname, item.name, settings=item.settings)
        backends.append(instance)
    return backends
