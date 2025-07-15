from django.db import models


class KindQuantity(models.TextChoices):
    KILOGRAMS = 'kg', 'Kilograms'
    LITERS = 'l', 'Liters'
    HUNDREDS = 'h', 'Hundreds'
    UNITS = 'u', 'Units'


class QuantityDisplayMixin:
    @property
    def quantity_display(self):
        measurement = getattr(self, 'measurement', None)
        quantity = getattr(self, 'quantity', None)
        kind_quantity = globals().get('KindQuantity')
        if measurement == kind_quantity.KILOGRAMS:
            return f"{quantity} kg"
        elif measurement == kind_quantity.LITERS:
            return f"{quantity} l"
        elif measurement == kind_quantity.HUNDREDS:
            return f"{quantity} hundreds"
        elif measurement == kind_quantity.UNITS:
            return f"{quantity / 100:.2f} hundreds"
        else:
            return str(quantity)
