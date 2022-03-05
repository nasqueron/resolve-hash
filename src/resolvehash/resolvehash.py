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

import yaml

from resolvehash.search import VcsHashSearch


#   -------------------------------------------------------------
#   Configuration
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_configuration_path():
    return os.environ["HOME"] + "/.config/resolve-hash.conf"


def parse_config():
    configuration_path = get_configuration_path()

    if not os.path.exists(configuration_path):
        return {}

    with open(get_configuration_path()) as fd:
        return yaml.safe_load(fd)


#   -------------------------------------------------------------
#   Hash search wrapper
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_search_classes():
    return [
        VcsHashSearch,
    ]


def find_hash(config, needle_hash):
    for search_class in get_search_classes():
        result = search_class(config, needle_hash).search()

        if result is not None:
            return result["url"]
