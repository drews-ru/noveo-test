from django.urls import path
from .views import listener, dispatcher


urlpatterns = [
    path('service/', listener, name='listener'),
    path('dispatcher/', dispatcher, name='dispatcher')
]