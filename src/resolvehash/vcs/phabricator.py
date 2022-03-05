#   -------------------------------------------------------------
#   Resolve hash :: VCS :: Phabricator
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Search hash on Phabricator
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import json
import requests


#   -------------------------------------------------------------
#   API mechanics
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def call_phabricator_api(api_url, token, method, parameters):
    parameters["api.token"] = token

    r = requests.post(api_url + method, data=parameters)
    if r.status_code != 200:
        return None

    result = r.json()["result"]
    if result:
        return result["data"]


#   -------------------------------------------------------------
#   API methods
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def query_phabricator_instance(api_url, token, commit_hash):
    result = call_phabricator_api(
        api_url,
        token,
        "diffusion.commit.search",
        {"constraints[identifiers][0]": commit_hash},
    )

    if result is None:
        return None

    try:
        commit = result[0]
    except IndexError:
        # Query works but didn't find anything
        return None

    return resolve_phabricator_commit_url(
        api_url, token, commit_hash, commit["fields"]["repositoryPHID"]
    )


def resolve_phabricator_commit_url(api_url, token, commit_hash, repository_phid):
    callsign = query_get_repository_callsign(api_url, token, repository_phid)

    return api_url.replace("api/", "") + callsign + commit_hash


def query_get_repository_callsign(api_url, token, repository_phid):
    result = call_phabricator_api(
        api_url,
        token,
        "diffusion.repository.search",
        {"constraints[phids][0]": repository_phid},
    )

    return "r" + result[0]["fields"]["callsign"]


#   -------------------------------------------------------------
#   Parse local configuration
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def query_phabricator_instances(config_file, commit_hash):
    with open(config_file, "r") as fd:
        instances = json.load(fd)

    for api_url, args in instances["hosts"].items():
        url = query_phabricator_instance(api_url, args["token"], commit_hash)
        if url is not None:
            return url
