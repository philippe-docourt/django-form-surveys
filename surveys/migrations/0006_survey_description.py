# Generated by Django 2.2.10 on 2022-02-08 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20220207_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='description',
            field=models.TextField(default=''),
        ),
    ]