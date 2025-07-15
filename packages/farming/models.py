from django.db import models

from packages.core.mixins import KindQuantity, QuantityDisplayMixin
from packages.production.models import Tree, Plot


# Create your models here.
class Harvest(models.Model, QuantityDisplayMixin):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=KindQuantity.choices, max_length=2,
                            default=KindQuantity.UNITS)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}({self.measurement}) on {self.harvest_date} from {self.plot.name}"

    def remaining_quantity(self):
        distributed = sum(d.quantity for d in self.distribution_set.all())
        return self.quantity - distributed

class Distribution(models.Model, QuantityDisplayMixin):
    class Type(models.TextChoices):
        SALE = 'sale', 'Sale'
        FAMILY = 'family', 'Family'
        DISCARD = 'discard'

    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    distribution_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=KindQuantity.choices, max_length=2,
                                      default=KindQuantity.UNITS)
    type = models.CharField(choices=Type.choices, max_length=10, default=Type.SALE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quality = models.CharField(max_length=100, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return (f"{self.harvest.plot.name} - {self.quality} - {self.quantity} "
                f" distributed as {self.get_type_display()} on {self.distribution_date}")

    def clean(self):
        # Ensure quantity does not exceed remaining harvest
        distributed = sum(d.quantity for d in self.harvest.distribution_set.exclude(pk=self.pk))
        remaining = self.harvest.quantity - distributed

        if self.quantity > remaining:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'quantity': f"Cannot distribute more than remaining ({remaining} {self.harvest.measurement})"
            })

    def save(self, *args, **kwargs):
        # Set measurement to match harvest before saving
        if self.measurement != self.harvest.measurement:
            self.measurement = self.harvest.measurement
        super().save(*args, **kwargs)
