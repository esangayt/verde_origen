from django.contrib import admin

from packages.production.models import Plot, Species, Tree

# change name in Django admin
admin.site.site_header = "Agro Management System"
admin.site.site_title = "Agro Management System Admin"


# Register your models here.
@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    pass

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    pass

@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'species', 'plot', 'date_planted', 'status',
                    'height_m', 'age_display', 'age_years')
    list_filter = ('species', 'plot', 'status')
