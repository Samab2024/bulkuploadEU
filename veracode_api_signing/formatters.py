# -*- coding: utf-8 -*-
# VERACODE.SOURCE.CONFIDENTIAL.VSSL-security-apisigning-python.b5f7196e3c8d51cae90d11c2f37240654e19bcc09da964086d43ce67f1f200de
#
# Copyright Veracode Inc., 2014


def format_signing_data(api_key_id, host, url, method):
    """ Format the input data for signing to the exact specification.

    Mainly, handles case-sensitivity where it must be handled.

    >>> format_signing_data('0123456789abcdef', 'veracode.com', '/home', 'GET')
    'id=0123456789abcdef&host=veracode.com&url=/home&method=GET'
    >>> format_signing_data('0123456789abcdef', 'VERACODE.com', '/home', 'get')
    'id=0123456789abcdef&host=veracode.com&url=/home&method=GET'
    """
    # Ensure some things are in the right case.
    # Note that path (url) is allowed to be case-sensitive (because path is sent along verbatim)
    # This is an HTTP fact, not a rule of our own design. stackoverflow.com/a/17113291/884640
    api_key_id = api_key_id.lower()
    host = host.lower()
    method = method.upper()

    # BTW we do not use a stdlib urlencode thing, because it is NOT exactly URL-encoded!
    return 'id={api_key_id}&host={host}&url={url}&method={method}'.format(api_key_id=api_key_id, host=host, url=url,
                                                                          method=method)


def format_veracode_hmac_header(auth_scheme, api_key_id, timestamp, nonce, signature):
    """ Given all the piecs including signature, just fit into the specified format.

    (This should _NOT_ manipulate case and so-on, that would likely break things.)

    >>> format_veracode_hmac_header(auth_scheme='VERACODE-HMAC-SHA-256', api_key_id='702a1650', \
                                    timestamp='1445452792746', nonce='3b1974fbaa7c97cc', \
                                    signature='b81c0315b8df360778083d1b408916f8')
    'VERACODE-HMAC-SHA-256 id=702a1650,ts=1445452792746,nonce=3b1974fbaa7c97cc,sig=b81c0315b8df360778083d1b408916f8'
    """
    return '{auth_scheme} id={id},ts={ts},nonce={nonce},sig={sig}'.format(auth_scheme=auth_scheme, id=api_key_id,
                                                                          ts=timestamp, nonce=nonce, sig=signature)
