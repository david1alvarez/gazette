# Generated by Django 3.2.4 on 2023-05-12 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city_manager', '0003_nullable_npc_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cities'},
        ),
    ]