# Generated by Django 3.1.6 on 2021-02-23 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210223_0552'),
        ('events', '0003_auto_20210223_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='events_registered', to='accounts.Team'),
        ),
    ]
