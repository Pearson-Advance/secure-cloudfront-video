"""
Amazon Cloudfront signed Video URLs.
"""
import logging

from botocore.signers import CloudFrontSigner
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect

from secure_cloudfront_video.exceptions import MissingCloudFrontInformationError
from secure_cloudfront_video.utils import cloudfront_rsa_signer, utc_time_plus_one_minute

log = logging.getLogger(__name__)


@login_required(redirect_field_name='dashboard')
def secure_cloudfront_video(request):
    """
    Generate a redirect to the AWS CloudFront resource.

    The signed resource URL must point to /secure-cloudfront-video/?key=path-to-aws-resource
    The resource URL will have a expiration time of one minute.
    Note that the resource URL must have the slash at the beginning of the string.

    **Example Requests**:

        GET lms-url/secure-cloudfront-video/?key=path-to-aws-resource

    **Responses**
        Redirect 302: If the signing process was successful and the resource exists.
        Not Found 404: If the 'key' query string or any of the Amazon Cloud Front settings is missing.
    """
    meta = request.META

    if not meta or meta.get('HTTP_HOST', '') not in meta.get('HTTP_REFERER', ''):
        raise Http404

    key = request.GET.get('key', '')
    cloudfront_url = getattr(settings, 'SCV_CLOUDFRONT_URL', '')
    cloudfront_id = getattr(settings, 'SCV_CLOUDFRONT_ID', '')

    if not (key and cloudfront_url and cloudfront_id):
        raise Http404

    try:
        cloudfront_signer = CloudFrontSigner(cloudfront_id, cloudfront_rsa_signer)
        redirect_url = cloudfront_signer.generate_presigned_url(
            url='{}{}'.format(cloudfront_url, key),
            date_less_than=utc_time_plus_one_minute(),
        )
    except MissingCloudFrontInformationError as cloudfront_error:
        log.error(str(cloudfront_error))
        raise Http404

    return redirect(redirect_url)
