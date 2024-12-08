from typing import Any
from django.contrib import admin
from .models import Kirjailija, Kirja, Laina
from datetime import datetime, timedelta


class KirjailijaAdmin(admin.ModelAdmin):
    list_display = ('etunimi', 'sukunimi')
    search_fields = ['etunimi', 'sukunimi']


class KirjaAdmin(admin.ModelAdmin):
    list_display = ('nimi', 'get_kirjailija', 'julkaisuvuosi', 'kustantaja')
    search_fields = ['nimi', 'kirjailija__sukunimi']
    list_filter = ['julkaisuvuosi', 'kustantaja']

    def get_kirjailija(self, obj):
        return ', '.join([
            kirjailija.etunimi + ' ' + kirjailija.sukunimi
            for kirjailija in obj.kirjailija.all()
        ])

    get_kirjailija.short_description = 'Kirjailija'


class LainaAdmin(admin.ModelAdmin):
    list_display = ('kirja', 'asiakas', 'lainauspaiva', 'palautuspaiva', 'is_returned')
    search_fields = ['kirja__nimi', 'asiakas__username', 'lainauspaiva', 'palautuspaiva']
    list_filter = ['asiakas__username', 'palautuspaiva']
    exclude = ('lainauspaiva', 'palautuspaiva')
    def save_model(self, request, obj, form, change):
        obj.lainauspaiva = datetime.now()
        obj.palautuspaiva = datetime.now() + timedelta(days=14)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('kirja', 'asiakas')


# Register your models here.
admin.site.register(Kirjailija, KirjailijaAdmin)
admin.site.register(Kirja, KirjaAdmin)
admin.site.register(Laina, LainaAdmin)
