from django.urls import path
from .views import listener


urlpatterns = [
    path('service/', listener, name='listener'),
]