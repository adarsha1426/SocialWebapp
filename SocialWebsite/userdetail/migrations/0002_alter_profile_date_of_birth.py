# Generated by Django 5.0.7 on 2024-08-29 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdetail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
