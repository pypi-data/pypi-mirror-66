from selia_visualizers.models import VisualizerComponentItemType


def get_visualizer(item_type):
    visualizer = VisualizerComponentItemType.objects.get(
        item_type=item_type,
        is_active=True)
    return visualizer
