# Generated by Django 5.2.1 on 2025-06-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartCity', '0012_progetto_totale_voti'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gestisce',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='votazione',
            name='data_voto',
            field=models.DateField(auto_now_add=True),
        ),
    ]
