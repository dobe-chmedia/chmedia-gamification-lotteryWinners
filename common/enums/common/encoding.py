##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""Defining the encodings"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-03-03          bettlerd    created script
##* 2023-07-13          bettlerd    added LATIN1 (iso-8859-1)
##* 2023-09-27          bettlerd    added UTF16
##*
##*

from enum import unique

from common.extensions.enum_extension import ExtendedEnum

@unique
class EncodingEnum(ExtendedEnum):
    """
    Defining the encodings
    """
    ASCII   = "ascii"
    LATIN1  = "iso-8859-1"
    UTF8    = "utf-8"
    UTF16   = "utf-16"