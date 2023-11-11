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


from api_jobs import ApiJobs
from constants_helper import ConstHelper


# NOTE: see constants_helper.py for constants you MUST setup


print("snapWONDERS Client OpenAPI v3 Python Example!")
print("You must set your API key and media path/filename")

# Create an analyse job and display results
ApiJobs.analyseJob(ConstHelper.MEDIA_PATH_FILENAME)