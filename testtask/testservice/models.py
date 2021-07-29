from django.db import models

# Notification model
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    received = models.DateTimeField(auto_now_add=True, verbose_name='Receive datetime')
    message = models.TextField(null=True, blank=True, verbose_name='Notification message')
    sender = models.CharField(max_length=255, null=True, blank=True, verbose_name='Sender name')
    sender_ip = models.CharField(max_length=15, null=True, blank=True, verbose_name='Sender IP address')

    def __str__(self):
        return f'[{self.received}] {self.message}'
