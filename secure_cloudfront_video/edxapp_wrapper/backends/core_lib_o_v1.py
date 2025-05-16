"""
Backend for openedx.core.lib modules.
"""

from openedx.core.lib.mobile_utils import is_request_from_mobile_app


def is_request_from_mobile_app_backend(request):
    """
    Backend function to check if the request is from a mobile app.
    """
    return is_request_from_mobile_app(request)
