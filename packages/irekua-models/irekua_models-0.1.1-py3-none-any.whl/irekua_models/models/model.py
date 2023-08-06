from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models.base import IrekuaModelBaseUser
from irekua_database.models import ItemType
from irekua_database.models import Term
from irekua_database.models import AnnotationType
from irekua_database.models import EventType


class Model(IrekuaModelBaseUser):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=('Name of the model.'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of the model.'),
        blank=True,
        null=True)
    repository = models.URLField(
        db_column='repository',
        verbose_name=_('repository'),
        help_text=_('URL for repository of model code.'),
        blank=False,
        null=False)

    annotation_type = models.ForeignKey(
        AnnotationType,
        on_delete=models.CASCADE,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation produced by the model.'),
        blank=False,
        null=False)

    item_types = models.ManyToManyField(
        ItemType,
        help_text=_('Item Types that can be processed by the model'),
        blank=True)
    event_types = models.ManyToManyField(
        EventType,
        help_text=_('Event types that can be detected by the model.'),
        blank=True)
    terms = models.ManyToManyField(
        Term,
        help_text=_('Terms that the model uses for its predictions.'),
        blank=True)

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ['-modified_on']

    def __str__(self):
        return self.name

    def validate_event_type(self, event_type):
        try:
            return self.event_types.get(name=event_type.name)
        except self.event_types.model.DoesNotExist:
            msg = _(
                'Event type %(event_type)s is invalid for model '
                '%(model)s')
            params = dict(event_type=str(event_type), model=str(self))
            raise ValidationError(msg, params=params)

    def validate_item_type(self, item_type):
        try:
            return self.item_types.get(name=item_type.name)
        except self.item_type.model.DoesNotExist:
            msg = _(
                'Item type %(item_type)s is invalid for model '
                '%(model)s')
            params = dict(item_type=str(item_type), model=str(self))
            raise ValidationError(msg, params=params)

    def validate_annotation_type(self, annotation_type):
        if self.annotation_type != annotation_type:
            msg = _(
                'Annotation type %(annotation_type)s is invalid for model '
                '%(model)s')
            params = dict(
                annotation_type=str(annotation_type),
                model=str(self))
            raise ValidationError(msg, params=params)

    def validate_labels(self, labels):
        for term in labels:
            if not self.terms.filter(pk=term.pk).exists():
                msg = _(
                    'Labels contain a term (%(term)s) that is not '
                    'valid for the model %(model)s')
                params = dict(term=term, model=self)
                raise ValidationError(msg, params=params)
