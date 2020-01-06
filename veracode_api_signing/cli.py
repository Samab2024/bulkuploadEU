# -*- coding: utf-8 -*-
# VERACODE.SOURCE.CONFIDENTIAL.VSSL-security-apisigning-python.b5f7196e3c8d51cae90d11c2f37240654e19bcc09da964086d43ce67f1f200de
#
# Copyright Veracode Inc., 2014
"""Print HMAC headers, for piping into curl, httpie, or other scripting uses.
.. moduleauthor:: Michael Floering <mfloering@veracode.com>

Usage:
    veracode_hmac_auth <http_method> <url>
    veracode_hmac_auth --help

Help:
    Print HMAC headers, for piping into curl, httpie, or other scripting uses.

    This module provides a low-level interface to generate Authorization headers
    for use Veracode's APIs at api.veracode.io.

    Given an HTTP method and URL, and given you have set up your credentials,
    you will get the value of an Authorization header printed out for your use.

    Before using, you must set up your API credentials as documented in this
    the Veracode Help Center. (As well as this project's README and
    the Veracode Internal Wiki.)

    Note that the scheme can only be HTTPS. 'https://' does not need to
    be provided, but it can be. 'http://' or other schemes
    are unsupported and an error will be raised.
"""
from __future__ import print_function
import docopt

from veracode_api_signing import validation
from veracode_api_signing.credentials import get_credentials
from veracode_api_signing.utils import get_host_from_url, get_path_and_params_from_url, get_scheme_from_url
from veracode_api_signing.veracode_hmac_auth import generate_veracode_hmac_header


def load_credentials_and_generate_hmac_header(http_method, url):
    """ Load credentials, (validate user-provided inputs), and generate HMAC header value.

    (This is distinct from the similar-but-different class in the other file, because
    that class is a plugin for `requests` ... in that case `requests` does the validation,
    so we don't have to.)
    """
    api_key_id, api_key_secret = get_credentials()

    if http_method:
        http_method = http_method.upper()
    else:
        raise ValueError('invalid HTTP method provided')

    scheme = get_scheme_from_url(url)
    if scheme:
        validation.validate_scheme(scheme)
    else:
        # note, we do NOT use urlparse/unparse because we want 0% chance of mangling things
        # in the path that could be sensitive to this. treat everything as raw as we can,
        # until the last moment possible. so, this is why we're using str.format() here.
        scheme = u'https'
        url = u'{}://{}'.format(scheme, url)

    host = get_host_from_url(url)
    if not host:
        raise ValueError("url parsing error: could not parse out host")

    path = get_path_and_params_from_url(url)
    if path is None:
        raise ValueError("url parsing error: could not parse out path")

    header_value = generate_veracode_hmac_header(
        host=host,
        path=path,
        method=http_method,
        api_key_id=api_key_id,
        api_key_secret=api_key_secret)

    return header_value


def main(args=None):
    if args is None:
        args = docopt.docopt(__doc__)

    http_method = args['<http_method>']
    url = args['<url>']

    header_value = load_credentials_and_generate_hmac_header(http_method, url)

    print(header_value, end="")


if __name__ == "__main__":
    main()
