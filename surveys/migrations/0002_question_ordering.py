# Generated by Django 2.2.10 on 2022-02-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='ordering',
            field=models.PositiveIntegerField(default=0),
        ),
    ]