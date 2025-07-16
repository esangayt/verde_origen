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

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'
    readonly_fields = ('total_price',)


@admin.register(SaleV2)
class SaleV2Admin(admin.ModelAdmin):
    list_display = ('date', 'total_earnings', 'total_sales', 'observations')
    search_fields = ('date',)
    readonly_fields = ('total_earnings', 'total_sales')
    ordering = ('-date',)
    list_filter = ('date',)
    inlines = [SaleDistributionInline]

    def total_sales(self, obj):
        total = sum([sd.total_price() for sd in obj.distributions.all()])
        return total
    total_sales.short_description = 'Total Sales'


@admin.register(SaleDistribution)
class SaleDistributionAdmin(admin.ModelAdmin):
    list_display = ('sale', 'distribution', 'price_per_hundred', 'observations')
    search_fields = ('sale__date', 'distribution__harvest__plot__name')
    list_filter = ('sale__date', 'distribution__type','distribution__harvest__plot__name')
    ordering = ('-sale__date',)

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = 'Total Price'