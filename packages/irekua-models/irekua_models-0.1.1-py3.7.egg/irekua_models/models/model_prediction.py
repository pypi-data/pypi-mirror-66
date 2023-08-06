from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models import Item
from irekua_database.models import Term
from irekua_database.models import EventType
from irekua_database.models.base import IrekuaModelBaseUser
from irekua_database.utils import empty_JSON


class ModelPrediction(IrekuaModelBaseUser):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Item on which the prediction was made.'),
        null=False,
        blank=False)
    model_version = models.ForeignKey(
        'ModelVersion',
        on_delete=models.PROTECT,
        db_column='model_version_id',
        verbose_name=_('model version'),
        help_text=_('Model and version used for this prediction'),
        blank=False,
        null=False)
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Event predicted by the model.'),
        blank=False,
        null=False)

    certainty = models.FloatField(
        db_column='certainty',
        verbose_name=_('certainty'),
        help_text=_('Model certainty of prediction. A number from 0 to 1.'),
        blank=False,
        null=False)
    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        default=empty_JSON,
        help_text=_('Information of annotation location within item'),
        blank=False,
        null=False)
    labels = models.ManyToManyField(
        Term,
        verbose_name=_('labels'),
        help_text=_('Terms used as labels to describe the predicted event.'),
        blank=False)

    class Meta:
        verbose_name = _('Model Prediction')
        verbose_name_plural = _('Model Predictions')
        ordering = ['-modified_on']

    def __str__(self):
        msg = _('Prediction of item %(item_id)s by model %(model)s')
        params = dict(item_id=self.item, model=self.model_version)
        return msg % params

    def clean(self):
        try:
            self.item.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        model = self.model_version.model
        try:
            model.validate_item_type(self.item.item_type)
        except ValidationError as error:
            raise ValidationError({'item': error})

        try:
            model.validate_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        annotation_type = self.model_version.model.annotation_type
        try:
            annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error})

        super().clean()
