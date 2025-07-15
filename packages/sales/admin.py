from django.contrib import admin

from packages.sales.models import Sale


# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'price_per_hundred', 'total_price', 'distribution', 'observations')
    search_fields = ('date', 'observations')
    list_filter = ('date', 'distribution__type')
    ordering = ('-date',)
