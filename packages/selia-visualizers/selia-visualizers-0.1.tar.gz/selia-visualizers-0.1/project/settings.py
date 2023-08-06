import os

from irekua_dev_settings.settings import *
from irekua_database.settings import *
from selia_visualizers.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]


INSTALLED_APPS = (
    SELIA_VISUALIZERS_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_BASE_APPS
)
