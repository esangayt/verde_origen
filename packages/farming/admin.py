from django.contrib import admin

from packages.farming.models import Harvest, Distribution
from .forms import DistributionInlineForm


# Inline for Distribution
class DistributionInline(admin.TabularInline):
    model = Distribution
    form = DistributionInlineForm
    fields = ('distribution_date', 'quantity', 'measurement', 'type', 'quality')
    extra = 0
    readonly_fields = ('measurement',)
    verbose_name_plural = 'Distribuciones'

# Register your models here.
@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ('id', 'harvest_date', 'quantity', 'quantity_display', 'measurement')
    #
    # def get_inline_instances(self, request, obj=None):
    #     if obj is None:
    #         return []
    #     return super().get_inline_instances(request, obj)
    #
    inlines = [DistributionInline]


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'harvest', 'distribution_date', 'quantity', 'measurement', 'quantity_display', 'type')
    readonly_fields = ('measurement',)
    list_filter = ('type',)
