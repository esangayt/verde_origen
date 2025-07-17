from django.db import models
from django.utils.translation import gettext_lazy as _

from packages.core.mixins import KindQuantity, QuantityDisplayMixin
from packages.production.models import Tree, Plot


# Create your models here.
class Harvest(models.Model, QuantityDisplayMixin):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=KindQuantity.choices, max_length=2, default=KindQuantity.UNITS)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return _("%(quantity)s(%(measurement)s) on %(date)s from %(plot)s") % {
            "quantity": self.quantity,
            "measurement": self.measurement,
            "date": self.harvest_date,
            "plot": self.plot.name
        }

    def remaining_quantity(self):
        distributed = sum(d.quantity for d in self.distribution_set.all())
        return self.quantity - distributed

class Distribution(models.Model, QuantityDisplayMixin):
    class Type(models.TextChoices):
        SALE = 'sale', _('Sale')
        FAMILY = 'family', _('Family')
        DISCARD = 'discard', _('Discard')

    class QualityChoices(models.TextChoices):
        EXCELLENT = 'excellent', _('Excellent')
        GOOD = 'good', _('Good')
        FAIR = 'fair', _('Fair')
        POOR = 'poor', _('Poor')

    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    distribution_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=KindQuantity.choices, max_length=2, default=KindQuantity.UNITS)
    type = models.CharField(choices=Type.choices, max_length=10, default=Type.SALE)
    quality = models.CharField(
        max_length=20,
        choices=QualityChoices.choices,
        default=QualityChoices.GOOD,
        blank=True,
        null=True
    )
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return (_("%(plot)s - %(quality)s - %(quantity)s distributed as %(type)s on %(date)s") % {
            "plot": self.harvest.plot.name,
            "quality": self.quality,
            "quantity": self.quantity,
            "type": self.get_type_display(),
            "date": self.distribution_date
        })

    def clean(self):
        # Ensure quantity does not exceed remaining harvest
        distributed = sum(d.quantity for d in self.harvest.distribution_set.exclude(pk=self.pk))
        remaining = self.harvest.quantity - distributed

        if self.quantity > remaining:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'quantity': _(f"Cannot distribute more than remaining ({remaining} {self.harvest.measurement})")
            })

    def save(self, *args, **kwargs):
        # Set measurement to match harvest before saving
        if self.measurement != self.harvest.measurement:
            self.measurement = self.harvest.measurement
        super().save(*args, **kwargs)
