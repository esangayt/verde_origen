from datetime import date
from django.utils.translation import gettext_lazy as _
from django.db import models


class Plot(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(_("Location"), max_length=255, blank=True, null=True)
    date_planted = models.DateField(_("Date planted"))
    observations = models.TextField(_("Observations"), blank=True, null=True)

    def __str__(self):
        return _("%(name)s - (%(area)s m²) with %(trees)s 🌳") % {
            "name": self.name,
            "area": self.area_m2 if self.area_m2 else "N/A",
            "trees": self.trees.count() if hasattr(self, 'trees') else 0
        }

    class Meta:
        verbose_name = _("Plot")
        verbose_name_plural = _("Plots")
        ordering = ['name']


class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Species")
        verbose_name_plural = _("Species")
        ordering = ['name']


class Tree(models.Model):
    class Status(models.TextChoices):
        HEALTHY = 'healthy', 'Healthy'
        DISEASED = 'diseased', 'Diseased'
        DEAD = 'dead', 'Dead'

    plot = models.ForeignKey(Plot, related_name='trees', on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    species = models.ForeignKey(Species, related_name='trees', on_delete=models.CASCADE)
    height_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_planted = models.DateField()
    age_years = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.HEALTHY)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.species}: {self.plot.name}"

    @property
    def age_display(self):
        if not self.date_planted:
            return ""

        today = date.today()
        years = today.year - self.date_planted.year
        months = today.month - self.date_planted.month
        if today.day < self.date_planted.day:
            months -= 1
        if months < 0:
            years -= 1
            months += 12
        return _("%(years)d years, %(months)d months") % {"years": years, "months": months}

    class Meta:
        verbose_name = _("Tree")
        verbose_name_plural = _("Trees")
        ordering = ['plot', 'species']
