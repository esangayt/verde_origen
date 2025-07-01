from django.db import models

from packages.production.models import Plot


class KindAgrochemical(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kind of Agrochemical"
        verbose_name_plural = "Kinds of Agrochemicals"
        ordering = ['name']


# Create your models here.
class Agrochemical(models.Model):
    class MeasurementUnit(models.TextChoices):
        KG = 'kg', 'Kilogram'
        L = 'l', 'Liter'
        G = 'g', 'Gram'

    name = models.CharField(max_length=100, unique=True)
    kind = models.ForeignKey(KindAgrochemical, related_name='supplies',
                             on_delete=models.CASCADE)
    measurement_unit = models.CharField(choices=MeasurementUnit.choices,
                                        max_length=2,
                                        default=MeasurementUnit.KG)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class ChemicalControl(models.Model):
    date = models.DateField()
    plot = models.ForeignKey(Plot, related_name='chemical_controls',
                             on_delete=models.CASCADE)
    agrochemical = models.ForeignKey(Agrochemical,
                                     related_name='chemical_controls',
                               on_delete=models.CASCADE)
    dosage = models.DecimalField(max_digits=10, decimal_places=2)
    responsible = models.CharField(max_length=100)
    observations = models.TextField(blank=True, null=True)