# Generated by Django 5.0.2 on 2024-03-22 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_id',
            field=models.PositiveIntegerField(default=0, unique=True),
        ),
    ]
