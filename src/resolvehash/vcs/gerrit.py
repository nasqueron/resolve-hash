#   -------------------------------------------------------------
#   Resolve hash :: VCS :: Gerrit
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Search hash on Gerrit
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import json
import requests


def query_gerrit_instance(instance, commit_hash):
    url = instance + "changes/?q=" + commit_hash
    r = requests.get(url)

    if r.status_code != 200:
        print(r.status_code)
        return None

    # We can't use r.json() as currently the API starts responses
    # by an extra line ")]}'"
    payload = r.text.strip().split("\n")[-1]
    result = json.loads(payload)

    if not result:
        return None

    change = result[0]
    return f"{instance}c/{change['project']}/+/{change['_number']}"


def query_gerrit_instances(instances, commit_hash):
    for instance in instances:
        url = query_gerrit_instance(instance, commit_hash)
        if url is not None:
            return url
