# Generated by Django 3.2.7 on 2021-10-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_bookedday'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
