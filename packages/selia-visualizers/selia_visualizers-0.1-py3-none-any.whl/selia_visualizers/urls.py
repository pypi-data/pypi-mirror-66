from django.urls import path
from selia_visualizers.views import get_visualizer


urlpatterns = [
    path('', get_visualizer, name='get_visualizer'),
]
