from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification, Backend
from .serializers import NotificationSerializer

import asyncio
from asgiref.sync import async_to_sync, sync_to_async

@async_to_sync
async def run_tasks(notification: NotificationSerializer):
#    backends = await get_backends()
#    print('async ', backends)
    loop = asyncio.get_event_loop()
    task = loop.create_task(sync_to_async(dispatch)(notification))
    loop.create_task(task_complete(task))


async def task_complete(task: asyncio.Task):
    await asyncio.sleep(5)
    if task.done():
        print('Dispatcher task completed: {}'.format(task.result()))
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
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Running dispatcher tasks
            run_tasks(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_backends():
    return Backend.objects.filter(enabled=True)


def dispatch(notification):
    """
    Dispatch notification to the registered and enabled backends
    """
    print('Dispatch run')

    queryset = Backend.objects.filter(enabled=True)

    print(backends)
    return 'ok'
    #return Response('ok', status=status.HTTP_200_OK)
