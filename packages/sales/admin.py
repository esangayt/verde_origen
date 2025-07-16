from django.contrib import admin

from packages.sales.models import Sale, SaleV2, SaleDistribution


# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'price_per_hundred', 'total_price', 'distribution', 'observations')
    search_fields = ('date', 'observations')
    list_filter = ('date', 'distribution__type')
    ordering = ('-date',)


class SaleDistributionInline(admin.TabularInline):
    model = SaleDistribution
    fields = ('distribution', 'price_per_hundred', 'total_price')
    extra = 1
    readonly_fields = ('total_price',)

@admin.register(SaleV2)
class SaleV2Admin(admin.ModelAdmin):
    list_display = ('date', 'total_earnings', 'observations')
    search_fields = ('date',)
    readonly_fields = ('total_earnings',)
    ordering = ('-date',)
    list_filter = ('date',)
    inlines = [SaleDistributionInline]


@admin.register(SaleDistribution)
class SaleDistributionAdmin(admin.ModelAdmin):
    list_display = ('sale', 'distribution', 'price_per_hundred','total_price', 'observations')
    search_fields = ('sale__date', 'distribution__harvest__plot__name')
    list_filter = ('sale__date', 'distribution__type', 'distribution__harvest__plot__name')
    ordering = ('-sale__date',)
