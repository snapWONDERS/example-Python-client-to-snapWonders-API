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


from constants_helper import ConstHelper


class ApiHelper:

    # The API URLs
    URL_SNAPWONDERS_API = "https://api.snapwonders.com/v1/"
    URL_UPLOAD_CREATE_MEDIA_URL = "upload/create-media-url"
    URL_JOB_CREATE_ANALYSE = "job/analyse"

    # Content types
    HTTP_CONTENT_TYPE_JSON = "application/json"

    # Job status
    JOB_STATUS_WAITING = "WAITING"
    JOB_STATUS_PROCESSING = "PROCESSING"
    JOB_STATUS_COMPLETED = "COMPLETED"


    # Adds the headers
    @staticmethod
    def add_api_headers(roHeaders, sContentType):

        if sContentType == None:
            roHeaders = {
                "Accept": "*/*",
                "Api_Key": ConstHelper.SNAPWONDERS_API_KEY
            }
        else:
            roHeaders = {
                "Accept": "*/*",
                "Api_Key": ConstHelper.SNAPWONDERS_API_KEY,
                "Content-Type": sContentType
            }

        return roHeaders
