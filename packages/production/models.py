from django.db import models

# Sumaq
# Palta
# Create your models here.
class Plot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_planted = models.DateField()
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Plot"
        verbose_name_plural = "Plots"
        ordering = ['name']


class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
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
    status =  models.CharField(max_length=20, choices=Status.choices, default=Status.HEALTHY)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.species} in {self.plot.name}"

    class Meta:
        verbose_name = "Tree"
        verbose_name_plural = "Trees"
        ordering = ['plot', 'species']