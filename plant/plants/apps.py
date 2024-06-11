import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlantsConfig(AppConfig):
    name = "plant.plants"
    verbose_name = _("Plants")

    def ready(self):
        with contextlib.suppress(ImportError):
            import plant.plants.signals  # noqa: F401
