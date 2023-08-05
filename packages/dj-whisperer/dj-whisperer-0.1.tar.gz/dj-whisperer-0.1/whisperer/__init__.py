from __future__ import unicode_literals


def autodiscover():
    from django.utils.module_loading import autodiscover_modules
    from whisperer.events import registry

    autodiscover_modules('webhooks', register_to=registry)


try:
    from whisperer.version import __version__
except ImportError:
    __version__ = '0.0.1'

__author__ = 'Akinon'
__license__ = 'MIT'
__maintainer__ = 'Akinon'
__email__ = 'dev@akinon.com'

default_app_config = 'whisperer.apps.WhispererConfig'
