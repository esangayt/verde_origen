from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HealthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'packages.health'
    verbose_name = _('health')
