# Generated by Django 4.2.2 on 2023-06-28 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventas_mes',
            old_name='mes',
            new_name='fecha',
        ),
    ]
