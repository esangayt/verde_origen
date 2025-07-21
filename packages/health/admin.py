from django.contrib import admin

from packages.health.models import Agrochemical, KindAgrochemical, ChemicalControl
from packages.production.models import Plot
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from django.utils import timezone
from django.contrib import admin
from django.http import HttpResponse

@admin.register(KindAgrochemical)
class KindAgrochemicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ChemicalControl)
class ChemicalControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'plot', 'agrochemical', 'dosage', 'unit', 'responsible')
    search_fields = ('plot__name', 'agrochemical__name', 'responsible', 'unit')
    list_filter = ('date', 'plot', 'agrochemical')
    ordering = ('-date',)


@admin.register(Agrochemical)
class AgrochemicalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kind', 'measurement_unit', 'stock')
    search_fields = ('name', 'kind__name')
    list_filter = ('kind', 'measurement_unit', 'kind__name')
    ordering = ('name',)
