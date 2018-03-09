from os.path import join

from uber.jinja import template_overrides
from uber.utils import mount_site_sections, static_overrides

from ._version import __version__  # noqa: F401
from .config import config


static_overrides(join(config['module_root'], 'static'))
template_overrides(join(config['module_root'], 'templates'))
mount_site_sections(config['module_root'])


# These need to come last so they can make use of config properties
from .models import *  # noqa: F401,E402,F403
from .model_checks import *  # noqa: F401,E402,F403
from .automated_emails import *  # noqa: F401,E402,F403


def on_load():
    """
    Called by sideboard when the plugin is loaded.

    This function is optional, and can be removed if not needed.
    """
    pass
