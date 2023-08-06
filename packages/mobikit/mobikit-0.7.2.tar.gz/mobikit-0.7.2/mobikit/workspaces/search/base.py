# Copyright (c) 2019 Mobikit, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import json
import requests
from mobikit.config import config
from mobikit.utils import token_required
from mobikit.exceptions import AuthException, MobikitException
from mobikit.workspaces.base import WorkspaceRef


@token_required
def search(keywords=None):
    """
    Function to allow a user to search for their workspaces with keywords.

    Parameters
    ----------
    keywords : str
        String of keywords

    Returns
    -------
    search_results : list<object>
    a list of workspaces
    """
    if not keywords:
        keywords = ""
    if not isinstance(keywords, str):
        raise MobikitException("pass in a string for keywords")
    query_string = {"query": keywords, "page_size": 100}
    try:
        f = requests.get(config.workspace_route, headers=config.headers, params=query_string)
        f.raise_for_status()
        search_results = []
        for workspace_result in json.loads(f.content):
            workspace = WorkspaceRef.create(workspace_result["id"])
            workspace.load(meta_only=True)
            search_results.append(
                {
                    "workspace_id": workspace.id,
                    "workspace_name": workspace.name,
                    "feeds": dict(workspace._feeds),
                }
            )
        config.logger.info(
            "your search yielded the following feeds: " + str(search_results)
        )
        return search_results
    except requests.exceptions.HTTPError as e:
        config.logger.exception(e)
        response_status = e.response.content if e.response is not None else "unknown"
        raise MobikitException(
            f"Received invalid response status code {response_status}."
        ) from e
    except requests.exceptions.RequestException as e:
        config.logger.exception(e)
        raise MobikitException(f"Error retrieving search results.") from e
