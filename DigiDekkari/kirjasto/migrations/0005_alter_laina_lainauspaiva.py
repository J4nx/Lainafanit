# Generated by Django 5.0.4 on 2024-04-24 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kirjasto', '0004_alter_laina_lainauspaiva_alter_laina_palautuspaiva'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laina',
            name='lainauspaiva',
            field=models.DateField(blank=True, null=True),
        ),
    ]