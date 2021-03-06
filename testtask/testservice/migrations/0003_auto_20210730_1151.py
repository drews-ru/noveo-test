# Generated by Django 3.2.5 on 2021-07-30 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testservice', '0002_alter_notification_sender_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backend',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Backend name')),
                ('enabled', models.BooleanField(default=True)),
                ('parameters', models.TextField(verbose_name='Backend parameters in JSON')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.CharField(max_length=255, null=True, verbose_name='Sender name'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, default='', verbose_name='Notification message'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender_ip',
            field=models.CharField(max_length=15, null=True, verbose_name='Sender IP address'),
        ),
    ]
