# Generated by Django 4.1.3 on 2022-12-12 19:42

import django.core.serializers.json
from django.db import migrations, models
import djf_surveys.models


class Migration(migrations.Migration):

    dependencies = [
        ("djf_surveys", "0010_model_translation"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="schema",
            field=models.JSONField(
                blank=True,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                help_text=djf_surveys.models.get_json_schema_help_text,
                null=True,
                verbose_name="schema",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="choices",
            field=models.TextField(
                blank=True,
                help_text="If type of field is radio, select, or multi select, fill in the options separated by commas or one item by line (allow usage of coma within proposition). Ex: Male, Female.",
                null=True,
                verbose_name="choices",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="help_text",
            field=models.TextField(
                blank=True,
                default="",
                help_text="You can add a help text in here.",
                max_length=400,
                verbose_name="help text",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="ordering",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Defines the question order within the surveys.",
                verbose_name="ordering",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="type_field",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Text"),
                    (1, "Number"),
                    (2, "Radio"),
                    (3, "Select"),
                    (4, "Multi Select"),
                    (5, "Text Area"),
                    (6, "URL"),
                    (7, "Email"),
                    (8, "Date"),
                    (10, "Time"),
                    (11, "Date and time"),
                    (9, "Rating"),
                    (12, "Color"),
                    (13, "JSON"),
                ],
                verbose_name="type of input field",
            ),
        ),
        migrations.AlterField(
            model_name="survey",
            name="description",
            field=models.TextField(
                default="", max_length=4096, verbose_name="description"
            ),
        ),
    ]
