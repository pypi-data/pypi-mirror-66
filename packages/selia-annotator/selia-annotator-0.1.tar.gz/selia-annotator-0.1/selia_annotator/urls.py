from django.urls import path
from selia_annotator import views


urlpatterns = [
    path(
        '',
        views.CollectionItemAnnotatorView.as_view(),
        name='annotator_app'),
    path('annotators/', views.get_annotator, name='get_annotator'),
]
