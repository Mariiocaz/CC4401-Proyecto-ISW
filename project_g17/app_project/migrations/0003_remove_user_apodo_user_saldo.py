# Generated by Django 4.2 on 2023-05-13 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_project', '0002_transaccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='apodo',
        ),
        migrations.AddField(
            model_name='user',
            name='saldo',
            field=models.FloatField(default=0),
        ),
    ]
