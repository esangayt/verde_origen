from django.db import models
from django.utils.translation import gettext_lazy as _


class KindQuantity(models.TextChoices):
    KILOGRAMS = 'kg', _('Kilograms')
    LITERS = 'l', _('Liters')
    HUNDREDS = 'h', _('Hundreds')
    UNITS = 'u', _('Units')


class QuantityDisplayMixin:
    @property
    def quantity_display(self):
        measurement = getattr(self, 'measurement', None)
        quantity = getattr(self, 'quantity', None)
        kind_quantity = globals().get('KindQuantity')
        if measurement == kind_quantity.KILOGRAMS:
            return _("%(quantity)s kg") % {"quantity": quantity}
        elif measurement == kind_quantity.LITERS:
            return _("%(quantity)s l") % {"quantity": quantity}
        elif measurement == kind_quantity.HUNDREDS:
            return _("%(quantity)s hundreds") % {"quantity": quantity}
        elif measurement == kind_quantity.UNITS:
            return _("%(quantity).2f hundreds") % {"quantity": quantity / 100}
        else:
            return str(quantity)

    quantity_display.fget.short_description = _("Quantity (display)")