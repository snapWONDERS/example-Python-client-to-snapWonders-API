#
# snapWONDERS OpenAPI Specification
# API version: 1.0
#
# Copyright (c) snapWONDERS.com, All rights reserved 2023
#
# Author: Kenneth Springer (https://kennethbspringer.au)
#
# All the snapWONDERS API services is available over the Clearnet / **Web** and Dark Web **Tor** and **I2P**
# Read details: https://snapwonders.com/snapwonders-openapi-specification
#
#


from os.path import getsize

from log_helper import LogHelper


class FileHelper:

    # Determine total file upload size
    @staticmethod
    def determineFileSize(sMediaPathFileName):

        nFileSize = getsize(sMediaPathFileName)
        if nFileSize <= 0:
            LogHelper.logAndExit(f"ERROR: Illegal file size:[{nFileSize}]")

        return nFileSize