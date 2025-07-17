from django.db import models
from django.utils.translation import gettext_lazy as _

from packages.farming.models import Distribution


# Create your models here.
class Sale(models.Model):
    date = models.DateField()
    price_per_hundred = models.DecimalField(max_digits=10, decimal_places=2)
    distribution = models.OneToOneField(Distribution, on_delete=models.PROTECT)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return _("Sale of %(quantity)s at %(price)s per hundred on %(date)s") % {
            "quantity": self.distribution.quantity,
            "price": self.price_per_hundred,
            "date": self.date
        }

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
        return _("Sale on %(date)s at %(earnings)s per hundred") % {
            "date": self.date,
            "earnings": self.total_earnings
        }

    def update_total_earnings(self):
        total = sum([d.total_price for d in self.distributions.all()])
        self.total_earnings = total
        self.save(update_fields=["total_earnings"])


class SaleDistribution(models.Model):
    sale = models.ForeignKey(SaleV2, on_delete=models.CASCADE, related_name='distributions')
    distribution = models.OneToOneField(Distribution, on_delete=models.CASCADE, limit_choices_to={'type': 'sale'})
    price_per_hundred = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observations = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = round(self.price_per_hundred * self.distribution.quantity / 100, 2)
        super().save(*args, **kwargs)
        self.sale.update_total_earnings()

    def delete(self, *args, **kwargs):
        sale = self.sale
        super().delete(*args, **kwargs)
        sale.update_total_earnings()

    def __str__(self):
        return _("Sale %(sale_id)s for Distribution %(dist_id)s") % {
            "sale_id": self.sale.id,
            "dist_id": self.distribution.id
        }
