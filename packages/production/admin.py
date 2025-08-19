from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from packages.production.models import Plot, Species, Tree
from .forms import PlotSalesFilterForm

# change name in Django admin
admin.site.site_header = _("Green always Management System Admin")
admin.site.site_title = _("Green always")


# Register your models here.
@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'area_m2', 'location', 'date_planted', 'trees_status_summary')
    search_fields = ('name', 'location')
    list_filter = ('date_planted',)
    ordering = ('name',)
    change_form_template = "admin/production/plot/change_form_with_pdf.html"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('trees')

    def trees_status_summary(self, obj):
        from django.db import models
        from django.utils.html import format_html
        status_colors = {
            'healthy': '#28a745',   # verde
            'diseased': '#ffc107', # amarillo
            'dead': '#dc3545',     # rojo
        }
        status_labels = {
            'healthy': _('healthy'),
            'diseased': _('diseased'),
            'dead': _('dead'),
        }
        status_counts = obj.trees.values('status').order_by('status').annotate(count=models.Count('id'))
        summary = []
        for entry in status_counts:
            status = entry['status']
            count = entry['count']
            color = status_colors.get(status, '#6c757d')
            label = status_labels.get(status, status)
            summary.append(f'<span style="display:inline-block;background:{color};color:white;padding:2px 8px;border-radius:8px;margin-right:4px;min-width:60px;text-align:center;">{label}: {count}</span>')
        return format_html(' '.join(summary)) if summary else '-'

    trees_status_summary.short_description = _("Number of Trees")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = PlotSalesFilterForm(request.GET or None)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'species', 'plot', 'date_planted', 'status', 'height_m', 'age_display')
    list_filter = ('species', 'plot', 'status')
