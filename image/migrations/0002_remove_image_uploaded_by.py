# Generated by Django 5.0 on 2024-01-26 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='uploaded_by',
        ),
    ]
