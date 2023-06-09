# Generated by Django 4.2.1 on 2023-07-12 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("city_manager", "0007_string_and_options_cleanup_3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="factionclock",
            name="faction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clocks_owned",
                to="city_manager.faction",
            ),
        ),
        migrations.AlterField(
            model_name="factionclock",
            name="target_faction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clocks_targeted_by",
                to="city_manager.faction",
            ),
        ),
        migrations.AlterField(
            model_name="factionfactionrelation",
            name="source_faction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relation_as_source_faction",
                to="city_manager.faction",
            ),
        ),
        migrations.AlterField(
            model_name="factionfactionrelation",
            name="target_faction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relation_as_target_faction",
                to="city_manager.faction",
            ),
        ),
    ]
