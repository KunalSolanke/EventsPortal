# Generated by Django 3.1.6 on 2021-02-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210223_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_id',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
