from django.contrib import admin
from selia_annotator import models


@admin.register(models.AnnotationToolComponent)
class AnnotatorAdmin(admin.ModelAdmin):
    pass
