from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models.base import IrekuaModelBaseUser


class ModelVersion(IrekuaModelBaseUser):
    model = models.ForeignKey(
        'Model',
        on_delete=models.CASCADE,
        db_column='model_id',
        verbose_name=_('model'),
        help_text=_('Model being versioned.'),
        null=False,
        blank=False)
    version = models.CharField(
        max_length=32,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of the model'),
        null=False,
        blank=False)

    class Meta:
        verbose_name = _('Model Version')
        verbose_name_plural = _('Model Versions')

        ordering = ['created_on', '-version']

        unique_together = [
            ['model', 'version']
        ]

    def __str__(self):
        return f'{str(self.model)} ({self.version})'
