# Generated by Django 5.0.4 on 2024-04-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kirjasto', '0003_remove_laina_lainaus_paiva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laina',
            name='lainauspaiva',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laina',
            name='palautuspaiva',
            field=models.DateField(blank=True, null=True),
        ),
    ]