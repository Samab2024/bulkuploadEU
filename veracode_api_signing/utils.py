# -*- coding: utf-8 -*-
# VERACODE.SOURCE.CONFIDENTIAL.VSSL-security-apisigning-python.b5f7196e3c8d51cae90d11c2f37240654e19bcc09da964086d43ce67f1f200de
#
# Copyright Veracode Inc., 2014

import os
import sys
import time
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_current_timestamp():
    return int(round(time.time() * 1000))


def generate_nonce():
    if sys.version_info >= (3,):
        return os.urandom(16).hex()
    else:
        return os.urandom(16).encode('hex')


def get_host_from_url(url):
    """
    >>> get_host_from_url('https://api.veracode.com/apm/v1/assets')
    'api.veracode.com'
    >>> get_host_from_url('https://api.veracode.com:12345/apm/v1/assets')
    'api.veracode.com'
    >>> get_host_from_url('whackabacka')
    """
    return urlparse(url).hostname


def get_path_and_params_from_url(url):
    """
    >>> get_path_and_params_from_url('https://api.veracode.com/apm/v1/assets')
    '/apm/v1/assets'
    >>> get_path_and_params_from_url('https://api.veracode.com:12345/apm/v1/assets')
    '/apm/v1/assets'
    >>> get_path_and_params_from_url('https://api.veracode.com:12345/')
    '/'
    >>> get_path_and_params_from_url('https://api.veracode.com:12345')
    ''
    >>> get_path_and_params_from_url('https://api.veracode.com:12345/apm/v1/assets?page=2')
    '/apm/v1/assets?page=2'
    >>> get_path_and_params_from_url('https://api.veracode.com:123/foo?pagesize=2&page=90')
    '/foo?pagesize=2&page=90'
    """
    parsed = urlparse(url)
    path = parsed.path
    if path is None:
        path = ''

    query = parsed.query
    if query:
        return '{}?{}'.format(path, query)
    else:
        return path


def get_scheme_from_url(url):
    """
    >>> get_scheme_from_url('http://api.veracode.com/apm/v1/assets')
    'http'
    >>> get_scheme_from_url('https://api.veracode.com:12345/apm/v1/assets')
    'https'
    >>> get_scheme_from_url('ftp://api.veracode.com:12345/apm/v1/assets')
    'ftp'
    >>> get_scheme_from_url('whackabacka')
    ''
    """
    scheme = urlparse(url).scheme
    return scheme
