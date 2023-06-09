# Generated by Django 4.2.1 on 2023-07-12 20:01

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("city_manager", "0004_districtless_landmark"),
    ]

    operations = [
        migrations.RenameField(
            model_name="faction",
            old_name="hold",
            new_name="hold_string",
        ),
        migrations.AlterField(
            model_name="city",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="buildings_description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="scene",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="streets",
            field=django_jsonform.models.fields.ArrayField(
                base_field=models.CharField(), blank=True, null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="district",
            name="streets_description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="district",
            name="traits",
            field=django_jsonform.models.fields.ArrayField(
                base_field=django_jsonform.models.fields.ArrayField(
                    base_field=models.CharField(), size=None
                ),
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="faction",
            name="assets",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="current_situation",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="headquarters",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="quirks",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="faction",
            name="turf",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="factionclock",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="factionclock",
            name="objective_type",
            field=models.IntegerField(
                choices=[
                    (1, "Acquire Asset"),
                    (2, "Contest Rival"),
                    (3, "Aid Ally"),
                    (4, "Remove Rival"),
                    (5, "Expand Gang"),
                    (6, "Claim Territory"),
                ],
                default=1,
            ),
        ),
        migrations.AlterField(
            model_name="landmark",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="landmark",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="person",
            name="adjectives",
            field=django_jsonform.models.fields.ArrayField(
                base_field=models.CharField(),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="person",
            name="name",
            field=models.CharField(default=""),
        ),
        migrations.AlterField(
            model_name="world",
            name="name",
            field=models.CharField(default=""),
        ),
    ]
