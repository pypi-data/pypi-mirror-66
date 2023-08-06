from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from selia_visualizers.utils import get_visualizer as get_visualizer_instance


@require_http_methods(["GET"])
def get_visualizer(request):
    item_type = request.GET.get('item_type', None)
    visualizer = get_visualizer_instance(item_type)

    response = {
        "visualizer": visualizer.visualizer_component.visualizer.pk,
        "file_url": visualizer.visualizer_component.javascript_file.url
    }
    return JsonResponse(response)
