#
# Copyright (c) 2019 Mobikit, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import pkg_resources
import json
import logging

import requests
import mobikit.workspaces as workspaces
from .config import config

# this will intentionally error for public release
# we don't want to expose models package to the public
try:
    from .models import models
except ImportError:
    pass

# instantiate logger
config.logger = logging.getLogger()
console = logging.StreamHandler()
config.logger.addHandler(console)

# load api urls based on environment
def set_config_uris(user_token=None):
    constants_file = pkg_resources.resource_filename(
        "mobikit",
        "reference/constants.json")

    with open(constants_file) as f:
        constants = json.load(f)
        config.headers = {'Authorization': f'Token {user_token}'}
        config.upload_route = config.base + constants["urls"]["upload_feed_route"]
        config.validate_route = config.base + constants["urls"]["validate"]
        config.workspace_route = config.base + constants["urls"]["workspace"]
        config.feed_route = config.base + constants["urls"]["feed"]
        config.query_route = config.base + constants["urls"]["query"]

# allow user to pass in an api key to get started
def set_api_key(user_token, api_url, **kwargs):
    if not isinstance(user_token, str):
        raise ValueError("Please pass in a string token.")

    if api_url:
        base = api_url
    else:
        base = "http://localhost:8000/"

    validation_uri = f"{base}api/users/token/validate/"
    headers = {"Authorization": "Token " + user_token}
    validation_status = requests.get(validation_uri, headers=headers).status_code
    if 200 < validation_status < 500:
        raise ValueError(
            "This is not a valid token. Did you specify the correct environment?"
        )
    if validation_status >= 500:
        raise RuntimeError("Unable to validate token. Please contact support.")

    config.logger.info("Token validated.")

    config.api_token = user_token
    config.base = base
    set_config_uris(user_token)
