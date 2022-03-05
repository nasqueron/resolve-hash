#   -------------------------------------------------------------
#   Resolve hash :: VCS :: GitLab
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Search hash on GitLab
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import requests


def query_gitlab_instance(instance, token, commit_hash):
    url = f"{instance}api/v4/search?scope=commits&search={commit_hash}"
    r = requests.get(url, headers={"PRIVATE-TOKEN": token})

    if r.status_code == 200:
        return None

    commits = r.json()
    if commits:
        return commits[0]["web_url"]
