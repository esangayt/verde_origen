from django.contrib import admin

from packages.health.models import Agrochemical, KindAgrochemical, \
    ChemicalControl

# Register your models here.
admin.site.register(Agrochemical)
admin.site.register(KindAgrochemical)
admin.site.register(ChemicalControl)