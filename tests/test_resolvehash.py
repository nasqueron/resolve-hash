#!/usr/bin/env python3

#   -------------------------------------------------------------
#   Resolve hash :: Tests
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Project:        Nasqueron
#   Description:    Query various sources with a known hash
#                   like Phabricator, Gerrit or GitHub to offer
#                   hash information URL from a VCS hash.
#   License:        BSD-2-Clause
#   -------------------------------------------------------------


import unittest
from builtins import staticmethod

from unittest_data_provider import data_provider

from resolvehash import resolvehash


class TestResolveHash(unittest.TestCase):
    def test_get_search_classes(self):
        search_classes = resolvehash.get_search_classes()
        self.assertTrue(type(search_classes) is list)

    @staticmethod
    def search_classes():
        return (tuple(resolvehash.get_search_classes()),)

    @data_provider(search_classes)
    def test_if_search_classes_provide_search_method(self, search_class):
        self.assertTrue(
            getattr(search_class, "search", None),
            f"The class `{search_class.__name__}` does NOT implement the method `search`.",
        )


if __name__ == "__main__":
    unittest.main()
