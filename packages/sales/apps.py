from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'packages.sales'
    verbose_name = _("sales")