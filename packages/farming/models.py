from django.db import models

from packages.production.models import Tree


# Create your models here.
class Harvest(models.Model):
    class KindQuantity(models.TextChoices):
        KILOGRAMS = 'kg', 'Kilograms'
        LITERS = 'l', 'Liters'
        HUNDREDS = 'h', 'Hundreds'

    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=KindQuantity.choices, max_length=2,
                            default=KindQuantity.HUNDREDS)
    quality = models.CharField(max_length=100, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tree.species.name} - {self.quantity} on {self.harvest_date}"

class Distribution(models.Model):
    # sometimes, not all harvest we will sale, same parts I will keep for myself
    # or I will give to my family, or I will discard
    class Type(models.TextChoices):
        SALE = 'sale', 'Sale'
        FAMILY = 'family', 'Family'
        DISCARD = 'discard'

    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE)
    distribution_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    measurement = models.CharField(choices=Harvest.KindQuantity.choices,
                             max_length=2,
                            default=Harvest.KindQuantity.HUNDREDS)
    type = models.CharField(choices=Type.choices, max_length=10, default=Type.SALE)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.harvest.tree.species.name} - {self.quantity} {self.get_measurement_display()} distributed as {self.get_type_display()} on {self.distribution_date}"
