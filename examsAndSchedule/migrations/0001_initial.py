# Generated by Django 4.1.4 on 2024-03-31 13:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
        ('subjects', '0001_initial'),
        ('school', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('totalMarks', models.CharField(blank=True, max_length=5, null=True)),
                ('startDateAndTime', models.DateTimeField(null=True)),
                ('endDateAndTime', models.DateTimeField(null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('courseID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='subjects.courses')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.session')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('classes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='classes.class')),
                ('courses', models.ManyToManyField(to='examsAndSchedule.courseschedule')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.session')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('marksType', models.CharField(blank=True, choices=[('MARKS', 'Marks'), ('GRADE', 'Grade'), ('PERCENTAGE', 'Percentage')], max_length=20, null=True)),
                ('marks', models.CharField(blank=True, max_length=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('CourseScheduleID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='examsAndSchedule.courseschedule')),
                ('examID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examsAndSchedule.exam')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.session')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='students.student')),
            ],
        ),
    ]
