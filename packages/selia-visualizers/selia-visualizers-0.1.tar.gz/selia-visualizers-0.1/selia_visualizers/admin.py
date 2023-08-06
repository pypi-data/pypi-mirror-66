from django.contrib import admin
from selia_visualizers import models


@admin.register(models.VisualizerComponent, models.VisualizerComponentItemType)
class VisualizersAdmin(admin.ModelAdmin):
    pass
