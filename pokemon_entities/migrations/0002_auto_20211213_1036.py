# Generated by Django 3.1.14 on 2021-12-13 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
