from django.db import models
from django.utils.translation import gettext_lazy as _
from packages.production.models import Plot


class KindAgrochemical(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Kind of Agrochemical')
        verbose_name_plural = _('Kinds of Agrochemicals')
        ordering = ['name']


# Create your models here.
class Agrochemical(models.Model):
    class MeasurementUnit(models.TextChoices):
        KG = 'kg', _('Kilogram')
        L = 'l', _('Liter')
        ML = 'ml', _('Milliliter')
        G = 'g', _('Gram')

    name = models.CharField(_('name'), max_length=100, unique=True)
    kind = models.ForeignKey(KindAgrochemical, related_name='supplies', on_delete=models.CASCADE,
                             verbose_name=_('kind'))
    measurement_unit = models.CharField(_('measurement unit'), choices=MeasurementUnit.choices, max_length=2,
                                        default=MeasurementUnit.KG)
    stock = models.PositiveIntegerField(_('stock'), default=0)

    class Meta:
        verbose_name = _('agrochemical')
        verbose_name_plural = _('agrochemicals')
        ordering = ['name']

    def __str__(self):
        return self.name


class ChemicalControl(models.Model):
    date = models.DateField(_('date'))
    plot = models.ForeignKey(Plot, related_name='plots_controls', on_delete=models.CASCADE, verbose_name=_('plot'))
    agrochemical = models.ForeignKey(Agrochemical, related_name='chemical_controls', on_delete=models.CASCADE,
                                     verbose_name=_('agrochemical'))
    dosage = models.DecimalField(_('dosage'), max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=10, choices=Agrochemical.MeasurementUnit.choices,
                            default=Agrochemical.MeasurementUnit.ML)
    responsible = models.CharField(_('responsible'), max_length=100)
    observations = models.TextField(_('observations'), blank=True, null=True)

    class Meta:
        verbose_name = _('chemical control')
        verbose_name_plural = _('chemical controls')
        ordering = ['-date']