import os

from irekua_dev_settings.settings import *
from irekua_database.settings import *
from irekua_models.settings import *
from irekua_rest_api.settings import *
from irekua_autocomplete.settings import *
from selia_templates.settings import *
from selia_visualizers.settings import *
from selia_annotator.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]


INSTALLED_APPS = (
    SELIA_ANNOTATOR_APPS +
    SELIA_VISUALIZERS_APPS +
    SELIA_TEMPLATES_APPS +
    IREKUA_REST_API_APPS +
    IREKUA_AUTOCOMPLETE_APPS +
    IREKUA_MODELS_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_BASE_APPS
)
