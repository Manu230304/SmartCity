# Generated by Django 5.2.1 on 2025-06-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartCity', '0028_alter_progetto_tecnico_approvatore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cittadino',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
