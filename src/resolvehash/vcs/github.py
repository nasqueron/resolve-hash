#   -------------------------------------------------------------
#   Resolve hash :: VCS :: GitHub
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Search hash on GitHub
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import requests


def query_github_instance(instance, commit_hash):
    url = f"{instance}/search/commits?q=hash:{commit_hash}"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    commits = r.json()["items"]
    if commits:
        return commits[0]["html_url"]
