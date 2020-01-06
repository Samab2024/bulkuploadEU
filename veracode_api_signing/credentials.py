# -*- coding: utf-8 -*-
# VERACODE.SOURCE.CONFIDENTIAL.VSSL-security-apisigning-python.b5f7196e3c8d51cae90d11c2f37240654e19bcc09da964086d43ce67f1f200de
#
# Copyright Veracode Inc., 2014

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
from os.path import expanduser

from .exceptions import VeracodeCredentialsError

PROFILE_DEFAULT = 'default'

ENV_API_KEY_NAME = 'VERACODE_API_KEY_ID'
ENV_API_SECRET_KEY_NAME = 'VERACODE_API_KEY_SECRET'
ENV_PROFILE = 'VERACODE_API_PROFILE'

FIX_INSTRUCTIONS = 'Please consult the documentation to get your Veracode credentials set up.'


def get_credentials(auth_file=None):
    """ Get credentials from supported sources. Precedence is 1) env vars, 2) file.
    """
    try:
        return get_credentials_from_environment_variables()
    except KeyError:
        pass
    return get_credentials_from_filesystem(auth_file)


def get_credentials_from_environment_variables():
    return os.environ[ENV_API_KEY_NAME], os.environ[ENV_API_SECRET_KEY_NAME]


def get_credentials_from_filesystem(auth_file=None):
    auth_file = auth_file or os.path.join('.', 'credentials')
    try:
        return get_credentials_from_config_file(auth_file)
    except (IOError, configparser.Error, configparser.NoSectionError) as e:
        raise VeracodeCredentialsError('Unable to get credentials from {file}: {error}'
                                       '\n{fix}'.format(file=auth_file, error=e, fix=FIX_INSTRUCTIONS))


def _get_credentials_profile():
    """ Get credentials profile from environment variable.
    """
    return os.environ.get(ENV_PROFILE, PROFILE_DEFAULT)


def get_credentials_from_config_file(auth_file):
    """ Get credentials from the config file. Uses the profile specified by env variable.
    """
    if not os.path.exists(auth_file):
        raise IOError("Could not read file: {}. {}".format(auth_file, FIX_INSTRUCTIONS))

    config = configparser.ConfigParser()
    config.read(auth_file)
    credentials_section_name = _get_credentials_profile()
    api_key_id = config.get(credentials_section_name, ENV_API_KEY_NAME)
    api_key_secret = config.get(credentials_section_name, ENV_API_SECRET_KEY_NAME)
    if api_key_id and api_key_secret:
        return api_key_id, api_key_secret
    else:
        raise VeracodeCredentialsError(
            'Unable to find credentials in auth file {auth_file}.\n{fix}'.format(
                auth_file=auth_file, fix=FIX_INSTRUCTIONS))
