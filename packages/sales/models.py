from django.db import models

from packages.farming.models import Distribution


# Create your models here.
class Sale(models.Model):
    date = models.DateField()
    price_per_hundred = models.DecimalField(max_digits=10, decimal_places=2)
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT)
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

