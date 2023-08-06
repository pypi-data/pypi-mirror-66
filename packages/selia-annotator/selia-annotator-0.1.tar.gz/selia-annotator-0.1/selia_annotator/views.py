from django.urls import reverse
from django.utils.html import mark_safe
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from irekua_database.models import Item
from selia_annotator.models import AnnotationToolComponent


@require_http_methods(["GET"])
def get_annotator(request):
    annotation_type = request.GET.get('annotation_type', None)
    annotator_component = get_object_or_404(
        AnnotationToolComponent,
        annotation_tool__annotation_type=annotation_type,
        is_active=True)

    response = {
        "annotation_tool": annotator_component.annotation_tool.pk,
        "file_url": annotator_component.javascript_file.url
    }
    return JsonResponse(response)


class CollectionItemAnnotatorView(TemplateView):
    template_name = 'selia_annotator/annotator.html'
    no_permission_template = 'selia_templates/generic/no_permission.html'

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        self.get_objects()

        return super().get(*args, **kwargs)

    def get_urls(self):
        collection = self.item.sampling_event_device.sampling_event.collection
        return {
            'terms_autocomplete': reverse(
                'irekua_autocomplete:term_autocomplete',
                args=[mark_safe('event_type_pk')]),
            'item': reverse(
                'irekua_rest_api:item-detail',
                args=[self.item.pk]),
            'item_type': reverse(
                'irekua_rest_api:itemtype-detail',
                args=[self.item.item_type.pk]),
            'annotation_types': reverse(
                'irekua_rest_api:collectiontype-annotation-types',
                args=[collection.collection_type.pk]),
            'annotations': reverse(
                'irekua_rest_api:item-annotations',
                args=[self.item.pk]),
            'annotation_detail': reverse(
                'irekua_rest_api:annotation-detail',
                args=[mark_safe('annotation_pk')]),
            'visualizers': reverse('selia_visualizers:get_visualizer'),
            'annotation_tools': reverse('selia_annotator:get_annotator'),
        }

    def get_objects(self):
        self.item = get_object_or_404(Item, pk=self.request.GET.get('pk', None))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['item'] = self.item
        context['sampling_event_device'] = self.item.sampling_event_device
        context['sampling_event'] = self.item.sampling_event_device.sampling_event
        context['collection'] = self.item.sampling_event_device.sampling_event.collection
        context['urls'] = self.get_urls()
        context["annotation_app_url"] = self.request.get_full_path
        return context
