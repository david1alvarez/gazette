# Generated by Django 3.2.4 on 2023-05-14 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city_manager', '0004_alter_city_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factionfactionrelation',
            name='source_faction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_source_faction', to='city_manager.faction'),
        ),
        migrations.AlterField(
            model_name='factionfactionrelation',
            name='target_faction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_target_faction', to='city_manager.faction'),
        ),
        migrations.CreateModel(
            name='FactionClock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('clock_segments', models.IntegerField(default=4)),
                ('objective_type', models.CharField(choices=[('ACQ', 'acquire asset'), ('CON', 'contest rival'), ('AID', 'aid ally'), ('REM', 'remove rival'), ('EXP', 'expand gang'), ('CLA', 'claim territory')], default='ACQ', max_length=3)),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clock_source_faction', to='city_manager.faction')),
                ('target_faction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clock_target_faction', to='city_manager.faction')),
            ],
        ),
    ]