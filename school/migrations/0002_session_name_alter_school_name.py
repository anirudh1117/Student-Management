# Generated by Django 4.1.4 on 2023-05-14 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
