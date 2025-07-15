from django.contrib import admin

from packages.farming.models import Harvest, Distribution


# Register your models here.
@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ('id', 'harvest_date', 'quantity', 'quantity_display', 'measurement')

    # def get_trees(self, obj):
    #     return ", ".join([str(tree) for tree in obj.tree.all()])
    # get_trees.short_description = 'Trees'


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'harvest', 'distribution_date', 'quantity', 'measurement', 'quantity_display', 'type')
    readonly_fields = ('measurement',)
    list_filter = ('type',)
