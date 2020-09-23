"""
Module containing helper and util functions for Amazon Cloudfront signed resource URLs views.
"""
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from django.conf import settings
from django.http import Http404

from secure_cloudfront_video.exceptions import MissingCloudFrontInformationError


def cloudfront_rsa_signer(message):
    """
    Its only input parameter will be the message to be signed,
    and its output will be the signed content as a binary string.
    The hash algorithm needed by CloudFront is SHA-1.

    More info: https://github.com/boto/botocore/blob/develop/botocore/signers.py#L274

    Returns:
        String that contains the signed private key.
    """
    cloudfront_key = str.encode(getattr(settings, 'SCV_CLOUDFRONT_PRIVATE_SIGNING_KEY', ''))

    if not cloudfront_key:
        raise MissingCloudFrontInformationError('Missing CloudFront private signing key.')

    private_key = serialization.load_pem_private_key(
        data=cloudfront_key,
        password=None,
        backend=default_backend(),
    )

    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def utc_time_plus_one_minute():
    """
    Return the UTC now time plus one minute.

    Returns:
        datetime.datetime instance that contains the UTC time plus one minute.
    """
    return datetime.utcnow() + timedelta(minutes=1)
