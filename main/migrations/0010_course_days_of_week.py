# Generated by Django 5.0.2 on 2024-04-12 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_course_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='days_of_week',
            field=models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=0, max_length=14),
        ),
    ]
