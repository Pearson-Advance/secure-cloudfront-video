# Open edX plugin to generate signed video URLs from Amazon Cloudfront.

## Features

- Creates a signed CloudFront URL based on given parameters.
- Creates an expiration time of one day for the video URL.

## Installation

### Open edX devstack

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart Lms/Studio services.

## Usage

To configure this plugin correctly you have to set:

- CLOUDFRONT_URL.
- CLOUDFRONT_ID.
- CLOUDFRONT_PRIVATE_SIGNING_KEY.

## Testing

- In Studio add a new video component to a course.
- Press the *Edit* button and then go to the *Advanced* section.
- In the *Video File URLs* field add the protected video. (e,g,. /secure-cloudfront-video/?key=*resource-id*/*resource-url*).
- Save the changes.
- Verify that the video is playable.
- Publish the changes.
- Login to the LMS, go to the course, and verify that the video is playable.

## Contributing

Add your contribution policy. (If required)
