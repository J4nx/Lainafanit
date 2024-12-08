from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Kirjailija(models.Model):
    etunimi = models.CharField(max_length=100, verbose_name=_("Etunimi"))
    sukunimi = models.CharField(max_length=100, verbose_name=_("Sukunimi"))

    class Meta:
        indexes = [
            models.Index(fields=['sukunimi'], name='sukunimi_idx'),
        ]

    def __str__(self):
        return f"{self.etunimi} {self.sukunimi}"


class Kirja(models.Model):
    nimi = models.CharField(max_length=100, verbose_name=_("Nimi"))
    kirjailija = models.ManyToManyField(Kirjailija,
                                        verbose_name=_("Kirjailija"))
    julkaisuvuosi = models.IntegerField(verbose_name=_("Julkaisuvuosi"))
    kuvaus = models.TextField(verbose_name=_("Kuvaus"))
    kustantaja = models.CharField(max_length=100, verbose_name=_("Kustantaja"))

    class Meta:
        indexes = [
            models.Index(fields=['julkaisuvuosi'], name='julkaisuvuosi_idx'),
            models.Index(fields=['nimi'], name='nimi_idx'),
        ]

    def __str__(self):
        kirjailijat_str = ', '.join([
            kirjailija.etunimi + ' ' + kirjailija.sukunimi
            for kirjailija in self.kirjailija.all()
        ])
        return f"{self.nimi} ({kirjailijat_str}), {self.julkaisuvuosi}"


class Laina(models.Model):
    asiakas = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name=_("Asiakas"))
    kirja = models.ForeignKey(Kirja,
                              on_delete=models.CASCADE,
                              verbose_name=_("Kirja"))
    lainauspaiva = models.DateField(null=True,
                                    blank=True,
                                    verbose_name=_("Lainauspäivä"))
    palautuspaiva = models.DateField(null=True,
                                     blank=True,
                                     verbose_name=_("Palautuspäivä"))
    palautettu = models.DateField(null=True,
                                  blank=True,
                                  verbose_name=_("Palautettu"))

    class Meta:
        indexes = [
            models.Index(fields=['palautettu'], name='palautettu_idx'),
            models.Index(fields=['asiakas', 'lainauspaiva'],
                         name='laina_asiakas_paiva_idx'),
        ]

    def __str__(self):
        return f"Laina ID: {self.id}, Asiakas ID: {self.asiakas_id}, Kirja ID: {self.kirja_id}"

    def is_returned(self):
        return self.palautettu is not None

    is_returned.boolean = True
    is_returned.short_description = _("Palautettu")
