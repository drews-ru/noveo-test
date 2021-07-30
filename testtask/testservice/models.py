from django.db import models

# Notification model
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    received = models.DateTimeField(auto_now_add=True, verbose_name='Receive datetime')
    message = models.TextField(blank=True, default='', verbose_name='Notification message')
    sender = models.CharField(max_length=255, null=True, verbose_name='Sender name')
    sender_ip = models.CharField(max_length=15, null=True, verbose_name='Sender IP address')

    def __str__(self):
        return f'[{self.received}] {self.message}'


# Generic backend model
class Backend(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, verbose_name='Backend name')
    enabled = models.BooleanField(default=True)
    parameters = models.TextField(null=False, verbose_name='Backend parameters in JSON')

    def __str__(self):
        return f'[{self.id}] {self.name}'
