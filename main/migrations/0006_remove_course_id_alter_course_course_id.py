# Generated by Django 5.0.2 on 2024-04-11 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_course_semester_course_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='id',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
