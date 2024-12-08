# Generated by Django 5.0.4 on 2024-04-24 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kirjasto', '0002_laina_palautettu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laina',
            name='lainaus_paiva',
        ),
        migrations.RemoveField(
            model_name='laina',
            name='palautus_paiva',
        ),
        migrations.AddField(
            model_name='laina',
            name='lainauspaiva',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='laina',
            name='palautuspaiva',
            field=models.DateField(null=True),
        ),
    ]
