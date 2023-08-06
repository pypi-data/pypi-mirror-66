from django.contrib import admin
from django import forms

from irekua_database.models import Term
from irekua_database.models import Item
from irekua_database.models import AnnotationType
from irekua_database.models import EventType
from irekua_database.models import ItemType
from irekua_models import models


class CustomModelAdmin(admin.ModelAdmin):
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(AnnotationType)
class AnnotationTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['id', 'item_type__name']


@admin.register(models.Model)
class ModelAdmin(CustomModelAdmin):
    search_fields = ['name']
    fields = (
        ('name', 'repository'),
        'description',
        ('annotation_type', 'item_types'),
        ('terms', 'event_types'),
    )
    autocomplete_fields = [
        'terms',
        'annotation_type',
        'event_types',
        'item_types']


@admin.register(models.ModelVersion)
class IrekuaModelsAdmin(CustomModelAdmin):
    search_fields = ['model__name']
    fields = (
        ('model', 'version'),)
    autocomplete_fields = ['model']


@admin.register(models.ModelPrediction)
class ModelPredictionAdmin(CustomModelAdmin):
    fields = (
        ('item', 'model_version', 'event_type'),
        'annotation',
        ('certainty', 'labels'))
    autocomplete_fields = [
        'item',
        'labels',
        'model_version',
        'event_type']
