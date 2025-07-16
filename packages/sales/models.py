from django.db import models

from packages.farming.models import Distribution


# Create your models here.
class Sale(models.Model):
    date = models.DateField()
    price_per_hundred = models.DecimalField(max_digits=10, decimal_places=2)
    distribution = models.OneToOneField(Distribution, on_delete=models.PROTECT)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f"Sale of {self.distribution.quantity} at {self.price_per_hundred} "
                f"per hundred "
                f"on {self.date}")

    @property
    def total_price(self):
        if self.distribution:
            return round(self.price_per_hundred * self.distribution.quantity / 100, 2)
        return 0


class SaleV2(models.Model):
    date = models.DateField()
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sale on {self.date} at {self.total_earnings} per hundred"


class SaleDistribution(models.Model):
    sale = models.ForeignKey(SaleV2, on_delete=models.CASCADE, related_name='distributions')
    distribution = models.OneToOneField(Distribution, on_delete=models.CASCADE, limit_choices_to={'type': 'sale'})
    price_per_hundred = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.TextField(blank=True, null=True)

    def total_price(self):
        return round(self.price_per_hundred * self.distribution.quantity / 100, 2)

    def __str__(self):
        return f"Sale {self.sale.id} for Distribution {self.distribution.id}"
