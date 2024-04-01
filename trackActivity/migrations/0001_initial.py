# Generated by Django 4.1.4 on 2024-03-31 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action_type', models.CharField(choices=[('Create', 'Create'), ('Read', 'Read'), ('Update', 'Update'), ('Delete', 'Delete'), ('Login', 'Login'), ('Logout', 'Logout'), ('Login Failed', 'Login Failed')], max_length=15)),
                ('action_time', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed')], default='Success', max_length=7)),
                ('data', models.JSONField(default=dict)),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.school')),
            ],
        ),
    ]
