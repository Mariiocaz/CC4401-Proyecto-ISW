# Generated by Django 4.2 on 2023-06-02 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_project', '0011_alter_transaccion_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaccion',
            name='fecha_creacion',
            field=models.DateField(default='2023-06-02'),
        ),
    ]
