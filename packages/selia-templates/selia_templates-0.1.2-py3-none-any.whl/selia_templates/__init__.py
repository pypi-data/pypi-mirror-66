import os
from .version import __version__


APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
default_app_config = 'selia_templates.apps.SeliaTemplatesConfig'
