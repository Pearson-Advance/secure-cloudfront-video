"""
Amazon Cloudfront signed Video URLs.
"""
import logging

from botocore.signers import CloudFrontSigner
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from secure_cloudfront_video.exceptions import MissingCloudFrontInformationError
from secure_cloudfront_video.utils import cloudfront_rsa_signer, utc_time_plus_one_day
from secure_cloudfront_video.edxapp_wrapper.core_lib import is_request_from_mobile_app

log = logging.getLogger(__name__)


def secure_cloudfront_video(request):
    """
    Generate a redirect to the AWS CloudFront resource.

    The signed resource URL must point to /secure-cloudfront-video/?key=path-to-aws-resource
    The resource URL will have a expiration time of one day.
    Note that the resource URL must have the slash at the beginning of the string.

    Due to the way that edx mobile apps work, the request from the mobile app must be unauthenticated
    whereas the web request must be authenticated.

    **Example Requests**:

        GET lms-url/secure-cloudfront-video/?key=path-to-aws-resource

    **Responses**
        Redirect 302: If the signing process was successful and the resource exists.
        Not Found 404: If the 'key' query string or any of the Amazon Cloud Front settings is missing.
    """
    if not is_request_from_mobile_app(request) and not request.user.is_authenticated:
        log.info('Request is not authenticated or from mobile app.')
        raise Http404

    key = request.GET.get('key', '')
    cloudfront_url = getattr(settings, 'SCV_CLOUDFRONT_URL', '')
    cloudfront_id = getattr(settings, 'SCV_CLOUDFRONT_ID', '')

    if not (key and cloudfront_url and cloudfront_id):
        log.info('Missing parameters for Cloudfront.')
        raise Http404

    try:
        cloudfront_signer = CloudFrontSigner(cloudfront_id, cloudfront_rsa_signer)
        redirect_url = cloudfront_signer.generate_presigned_url(
            url='{}{}'.format(cloudfront_url, key),
            date_less_than=utc_time_plus_one_day(),
        )
    except MissingCloudFrontInformationError as cloudfront_error:
        log.error(str(cloudfront_error))
        raise Http404

    return redirect(redirect_url)
