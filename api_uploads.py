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


import json

from http import HTTPStatus
from io import BytesIO
from os.path import basename
from requests import Session

from api_helper import ApiHelper
from constants_helper import ConstHelper
from file_helper import FileHelper
from log_helper import LogHelper


class ApiUpload:

    oClient_ = Session()

    # Create an upload media URL
    @staticmethod
    def createUploadMediaUrl(sMediaPathFileName):
        print("CALL: createUploadMediaUrl()")

        # Build up Json File Metadata
        oFileMetadata = {
            "name": basename(sMediaPathFileName),
            "size": FileHelper.determineFileSize(sMediaPathFileName)
        }
        sJsonFileMetadata = json.dumps(oFileMetadata)

        # Call API to create the media url for uploading
        oHeaders = {}
        oHeaders = ApiHelper.add_api_headers(oHeaders, ApiHelper.HTTP_CONTENT_TYPE_JSON)
        oResponse = ApiUpload.oClient_.post(url=ApiHelper.URL_SNAPWONDERS_API + ApiHelper.URL_UPLOAD_CREATE_MEDIA_URL,
                                            data=sJsonFileMetadata,
                                            headers=oHeaders)

        # Check POST status for errors
        if oResponse.status_code != HTTPStatus.CREATED:
            LogHelper.logAndExit(f"ERROR: Send POST request failed:[{oResponse.text}]")

        # Success - Extract the media url
        sUrlCreateMedia = oResponse.headers["Location"]
        print(f"SUCCESS: Created resumable uploading media url:[{sUrlCreateMedia}]")
        return sUrlCreateMedia


    # Uploads file to given media url
    @staticmethod
    def uploadMedia(sUrlUploadMedia, sMediaPathFileName):
        print("CALL: uploadMedia()")

        # Open file
        try:
            with open(sMediaPathFileName, "rb") as oFile:
                arrBytesData = oFile.read()
        except Exception as oEx:
            LogHelper.logAndExit(f"ERROR: Open file failed:[{oEx}]")

        # Loop through each chunk and upload
        nOffset = 0
        for arrDataChunk in ApiUpload.createDataChunk(arrBytesData, ConstHelper.DATA_CHUNK_SIZE):
            nOffset = ApiUpload.uploadDataChunk(sUrlUploadMedia, arrDataChunk, nOffset)

        print(f"SUCCESS: Uploaded file:[{sMediaPathFileName}] to media url:[{sUrlUploadMedia}]")


    # Uploads a data chunk
    @staticmethod
    def uploadDataChunk(sUrlUploadMedia, arrDataChunk, nOffset):

        # Build the multipart form data for uploading
        oMultipartData = {
            "offset": nOffset ,
            "file": BytesIO(arrDataChunk)
        }

        # Patch the data chunk for uploading to given media url
        oHeaders ={}
        oHeaders = ApiHelper.add_api_headers(oHeaders, None)
        oResponse = ApiUpload.oClient_.patch(sUrlUploadMedia, files=oMultipartData, headers=oHeaders)

        if oResponse.status_code != HTTPStatus.OK:
            LogHelper.logAndExit("ERROR: Upload data chunk failed")

	    # Check for upload errors.
	    # Note: If an upload failed, you can retry uploading from the last offset. Call the HEAD request to determine
	    # the last offset position if you are not sure what that is. Uploading is resumable and can be continued
	    # at a later time (which is useful if there is a network outage or connectivity issue)
	    # snapWONDERS uploading follows the Tus.io protocol
        nUploadOffset = int(oResponse.headers["Upload-Offset"])
        if nUploadOffset <= 0:
            LogHelper.logAndExit(f"ERROR: New `offset` extraction failed:[{nUploadOffset}]")
        elif nUploadOffset != (nOffset + len(arrDataChunk)):
            LogHelper.logAndExit("ERROR: Uploading data chunk failed! TODO: You can retry uploading the last data chunk or "
                                 + "resume uploading at a later point in time")

        # Success - Uploaded the data chunk
        print(f"INFO: Uploaded data chunk starting at offset:[{nOffset}], newOffset:[{nUploadOffset}]")
        return nUploadOffset


    # Creates a chunk data
    @staticmethod
    def createDataChunk(arrBytesData, nChunkSize):
        for nI in range(0, len(arrBytesData), nChunkSize):
            yield arrBytesData[nI:nI + nChunkSize]