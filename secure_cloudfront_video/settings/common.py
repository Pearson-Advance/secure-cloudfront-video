"""
Common Django settings for secure_cloudfront_video project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import unicode_literals

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'


# Application definition

INSTALLED_APPS = []

ROOT_URLCONF = 'secure_cloudfront_video.urls'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.SCV_CLOUDFRONT_ID = ''
    settings.SCV_CLOUDFRONT_URL = ''
    settings.SCV_CLOUDFRONT_PRIVATE_SIGNING_KEY = ''
    settings.SCV_CORE_LIB_BACKEND = 'secure_cloudfront_video.edxapp_wrapper.backends.core_lib_o_v1'  # pylint: disable=line-too-long
