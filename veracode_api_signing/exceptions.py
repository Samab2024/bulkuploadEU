# -*- coding: utf-8 -*-
# VERACODE.SOURCE.CONFIDENTIAL.CTO-CloudAtlas.b5f7196e3c8d51cae90d11c2f37240654e19bcc09da964086d43ce67f1f200de
#
# Copyright Veracode Inc., 2014


class VeracodeAPISigningException(Exception):
    """
    Thrown if anything goes wrong in this library
    """
    pass


class VeracodeCredentialsError(VeracodeAPISigningException):
    """
    Thrown if there is anything Veracode credentials, such as not found, improper format ... etc
    """
    pass


class UnsupportedAuthSchemeException(VeracodeAPISigningException):
    """
    Thrown if there is anything Veracode credentials, such as not found, improper format ... etc
    """
    pass
