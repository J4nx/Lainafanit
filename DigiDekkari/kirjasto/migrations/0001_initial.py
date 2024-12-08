# Generated by Django 5.0.4 on 2024-04-15 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kirjailija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etunimi', models.CharField(max_length=100)),
                ('sukunimi', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kirja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=100)),
                ('julkaisuvuosi', models.IntegerField()),
                ('kuvaus', models.TextField()),
                ('kansikuva', models.ImageField(blank=True, null=True, upload_to='kansikuvat/')),
                ('kustantaja', models.CharField(max_length=100)),
                ('kirjailija', models.ManyToManyField(to='kirjasto.kirjailija')),
            ],
        ),
        migrations.CreateModel(
            name='Laina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lainaus_paiva', models.DateField()),
                ('palautus_paiva', models.DateField()),
                ('asiakas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kirja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kirjasto.kirja')),
            ],
        ),
    ]