# Generated by Django 4.2 on 2023-05-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_project', '0007_user_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, primary_key=True, serialize=False),
        ),
    ]
