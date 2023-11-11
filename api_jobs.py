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
import time

from http import HTTPStatus
from os.path import basename
from requests import Session

from api_helper import ApiHelper
from api_uploads import ApiUpload
from log_helper import LogHelper


class ApiJobs:

    oClient_ = Session()

    # Create an analyse job and display results
    @staticmethod
    def analyseJob(sPathFileName):

        # Create upload media url and upload file in data chunks
        sUrlUploadMedia = ApiUpload.createUploadMediaUrl(sPathFileName)
        ApiUpload.uploadMedia(sUrlUploadMedia, sPathFileName)

        # Create an analyse job url
        sUrlJobStatus = ApiJobs.createAnalyseJob(sUrlUploadMedia)

        # Track the job status, wait until analyse job is completed
        oJobStatus = ApiJobs.getJobStatus(sUrlJobStatus)

        # Wait for the job to be completed
        while oJobStatus["status"] in [ApiHelper.JOB_STATUS_WAITING, ApiHelper.JOB_STATUS_PROCESSING]:
             print("INFO: Sleeping for a few seconds...")
             time.sleep(5)
             oJobStatus = ApiJobs.getJobStatus(sUrlJobStatus)

        # Some unknown state?
        if oJobStatus["status"] != ApiHelper.JOB_STATUS_COMPLETED:
            LogHelper.logAndExit(f"ERROR: Analyse job failed with status:[{oJobStatus['status']}], message:[{oJobStatus['message']}]")

        # Get and display results
        sUrlResult = ApiJobs.getJobResults(oJobStatus["resultUrl"])
        oResult = json.loads(sUrlResult)
        sJsonResult = json.dumps(oResult, indent=2)

        # NOTE: You can call getJobResults() for image url resources contained within the JSON result
        print(sJsonResult)


    # Create an analyse job
    @staticmethod
    def createAnalyseJob(url_upload_media):
        print("CALL: createAnalyseJob()")

        # Build up Json Analyse Job
        oJobAnalyse = {
            "key": basename(url_upload_media),
            "enableTips": True,
            "enableExtraAnalysis": True
        }
        sJsonJobAnalyse = json.dumps(oJobAnalyse)

        # Call API to create an analyse job
        oHeaders = {}
        oHeaders = ApiHelper.add_api_headers(oHeaders, ApiHelper.HTTP_CONTENT_TYPE_JSON)
        oResponse = ApiJobs.oClient_.post(ApiHelper.URL_SNAPWONDERS_API + ApiHelper.URL_JOB_CREATE_ANALYSE,
                                          data=sJsonJobAnalyse,
                                          headers=oHeaders)

        # Check POST status for errors
        if oResponse.status_code != HTTPStatus.OK:
            LogHelper.logAndExit(f"Create analyse job failed:[{oResponse.text}]")

        # Success - Extract the media url
        sUrlJobAnalyse = oResponse.headers["Location"]
        print(f"SUCCESS: Created analyse job located at url:[{sUrlJobAnalyse}]")
        return sUrlJobAnalyse


    # Gets the job status
    @staticmethod
    def getJobStatus(sUrlJobStatus):
        print("CALL: getJobStatus()")

        # Call API to get job status
        oHeaders = {}
        oHeaders = ApiHelper.add_api_headers(oHeaders, ApiHelper.HTTP_CONTENT_TYPE_JSON)
        oResponse = ApiJobs.oClient_.post(sUrlJobStatus, headers=oHeaders)

        # Check POST status for errors
        if oResponse.status_code != HTTPStatus.OK:
            LogHelper.logAndExit(f"Get job status failed:[{oResponse.text}]")

        # Success - Extract job status
        oJobStatus = oResponse.json()
        print(f"SUCCESS: Have job status:[{oJobStatus['status']}]")
        return oJobStatus


    # Gets the job results (this can be a JSON or image content)
    @staticmethod
    def getJobResults(url_job_results):
        print("CALL: getJobResult()")

        # Call API to get job status
        oHeaders = {}
        oHeaders = ApiHelper.add_api_headers(oHeaders, ApiHelper.HTTP_CONTENT_TYPE_JSON)
        oResponse = ApiJobs.oClient_.get(url_job_results, headers=oHeaders)

        # Check GET status for errors
        if oResponse.status_code != HTTPStatus.OK:
            LogHelper.logAndExit(f"Get job results failed:[{oResponse.text}]")

        # Success - Extract the job results
        return oResponse.text