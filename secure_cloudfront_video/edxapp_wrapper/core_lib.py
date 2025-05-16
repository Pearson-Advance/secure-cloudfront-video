"""
Backend definitions for openedx.core.lib modules.
"""

from importlib import import_module

from django.conf import settings


def is_request_from_mobile_app(request):
    """
    Check if the request is from a mobile app using the backend.
    """
    backend = import_module(settings.SCV_CORE_LIB_BACKEND)

    return backend.is_request_from_mobile_app_backend(request)
