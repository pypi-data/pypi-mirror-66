import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import ItemType
from irekua_database.models import Visualizer


def visualizer_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'visualizers/{name}_{version}.{ext}'.format(
        name=instance.visualizer.name.replace(' ', '_'),
        version=instance.visualizer.version.replace('.', '_'),
        ext=ext)


class VisualizerComponent(models.Model):
    visualizer = models.OneToOneField(
        Visualizer,
        on_delete=models.CASCADE,
        db_column='visualizer_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer'),
        blank=False,
        null=False)
    javascript_file = models.FileField(
        upload_to=visualizer_path,
        db_column='javascript_file',
        verbose_name=_('javascript file'),
        help_text=_('Javascript file containing visualizer component'),
        blank=False,
        null=False)

    item_types = models.ManyToManyField(
        ItemType,
        through='VisualizerComponentItemType',
        through_fields=('visualizer_component', 'item_type'))

    class Meta:
        verbose_name = _('Visualizer Component')
        verbose_name_plural = _('Visualizers Components')

    def __str__(self):
        return str(self.visualizer)


class VisualizerComponentItemType(models.Model):
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item type'))
    visualizer_component = models.ForeignKey(
        'VisualizerComponent',
        on_delete=models.CASCADE,
        db_column='visualizer_component_id',
        verbose_name=_('visualizer component'),
        help_text=_('Visualizer component'))

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_('Is visualizer app active?'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Visualizer Component Item Type')
        verbose_name_plural = _('Visualizer Component Item Types')

        unique_together = (
            ('item_type', 'visualizer_component'),
        )

    def deactivate(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            queryset = VisualizerComponentItemType.objects.filter(
                item_type=self.item_type, is_active=True)
            for entry in queryset:
                if entry != self:
                    entry.deactivate()

        super().save(*args, **kwargs)
