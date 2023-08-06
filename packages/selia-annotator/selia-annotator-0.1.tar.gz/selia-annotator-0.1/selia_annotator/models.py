import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import AnnotationTool


def annotator_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'annotators/{name}_{version}.{ext}'.format(
        name=instance.annotation_tool.name.replace(' ', '_'),
        version=instance.annotation_tool.version.replace('.', '_'),
        ext=ext)


class AnnotationToolComponent(models.Model):
    annotation_tool = models.OneToOneField(
        AnnotationTool,
        on_delete=models.CASCADE,
        db_column='annotation_tool_id',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool'),
        blank=False,
        null=False)
    javascript_file = models.FileField(
        upload_to=annotator_path,
        db_column='javascript_file',
        verbose_name=_('javascript file'),
        help_text=_('Javascript file containing annotator component'),
        blank=False,
        null=False)

    is_active = models.BooleanField(
        db_column='is_active',
        verbose_name=_('is active'),
        help_text=_('Is annotator tool active?'),
        default=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Annotation Tool Component')
        verbose_name_plural = _('Annotation Tool Components')

    def deactivate(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.is_active:
            queryset = AnnotationToolComponent.objects.filter(
                annotation_tool__annotation_type=self.annotation_tool.annotation_type,
                is_active=True)
            for entry in queryset:
                if entry != self:
                    entry.deactivate()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.annotation_tool)
