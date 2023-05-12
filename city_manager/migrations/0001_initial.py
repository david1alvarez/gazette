# Generated by Django 3.2.4 on 2023-05-12 01:33

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('scene', models.TextField(blank=True, null=True)),
                ('streets_description', models.TextField(blank=True, null=True)),
                ('streets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('buildings_description', models.TextField(blank=True, null=True)),
                ('traits', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None), size=None)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='city_manager.city')),
            ],
        ),
        migrations.CreateModel(
            name='Faction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('tier', models.IntegerField(default=0)),
                ('hold', models.CharField(choices=[('w', 'weak'), ('s', 'strong')], default='w', max_length=1)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('turf', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('headquarters', models.CharField(blank=True, max_length=100, null=True)),
                ('assets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('quirks', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='city_manager.city')),
            ],
        ),
        migrations.CreateModel(
            name='NonPlayerCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('adjectives', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='city_manager.district')),
            ],
        ),
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='city_manager.district')),
            ],
        ),
        migrations.CreateModel(
            name='FactionFactionRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_reputation', models.IntegerField(default=0)),
                ('source_faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_faction', to='city_manager.faction')),
                ('target_faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_faction', to='city_manager.faction')),
            ],
        ),
        migrations.CreateModel(
            name='DistrictFaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_manager.district')),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city_manager.faction')),
            ],
        ),
    ]
