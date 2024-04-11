# Generated by Django 5.0.2 on 2024-04-11 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_professor_email_professor_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=100)),
                ('room_number', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]