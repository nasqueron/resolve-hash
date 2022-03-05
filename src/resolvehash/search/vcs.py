#   -------------------------------------------------------------
#   Resolve hash
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Query various sources with a known hash
#                   like Phabricator, Gerrit or GitHub to offer
#                   hash information URL from a VCS hash.
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import os

from resolvehash.vcs import gerrit
from resolvehash.vcs import github
from resolvehash.vcs import gitlab
from resolvehash.vcs import phabricator


class VcsHashSearch:
    def __init__(self, config, needle_hash):
        self.config = config
        self.hash = needle_hash

    def search_phabricator(self):
        arc_rc_path = os.environ["HOME"] + "/.arcrc"
        if os.path.exists(arc_rc_path):
            return phabricator.query_phabricator_instances(arc_rc_path, self.hash)

    def search_gerrit(self):
        if "gerrit" in self.config:
            return gerrit.query_gerrit_instances(self.config["gerrit"], self.hash)

    def search_github(self):
        return github.query_github_instance("https://api.github.com", self.hash)

    def search_gitlab(self):
        if "gitlab_public_token" in self.config:
            return gitlab.query_gitlab_instance(
                "https://gitlab.com/", self.config["gitlab_public_token"], self.hash
            )

    def get_search_methods(self):
        return {
            # Strategy A. Code review systems we can autodiscover
            "Phabricator": self.search_phabricator,
            # Strategy B. Sources explicitly configured in configuration
            "Gerrit": self.search_gerrit,
            # Strategy C. Popular public hosting sites
            "GitHub": self.search_github,
            "GitLab": self.search_gitlab,
        }

    def search(self):
        for source, method in self.get_search_methods().items():
            result = method()
            if result:
                return {
                    "search": "vcs",
                    "source": source,
                    "url": result,
                }
