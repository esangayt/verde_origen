from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from packages.production.models import Plot, Species, Tree

# change name in Django admin
admin.site.site_header = _("Green always Management System Admin")
admin.site.site_title = _("Green always")


# Register your models here.
@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'area_m2', 'location', 'date_planted')
    search_fields = ('name', 'location')
    list_filter = ('date_planted',)
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('trees')

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'species', 'plot', 'date_planted', 'status', 'height_m', 'age_display')
    list_filter = ('species', 'plot', 'status')
