from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^annotator/', include(('selia_annotator.urls', 'selia_annotator'))),
    url(r'^api/', include('irekua_rest_api.urls')),
    url(r'^autocomplete/', include(('irekua_autocomplete.urls', 'irekua_autocomplete'))),
    url(r'^visualizers/', include(('selia_visualizers.urls', 'selia_visualizers'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
