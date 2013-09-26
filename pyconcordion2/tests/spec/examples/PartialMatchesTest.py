from __future__ import unicode_literals

from base import ConcordionTestCase


class PartialMatchesTest(ConcordionTestCase):
    def setUp(self):
        self.usernames = []

    def setUpUser(self, username):
        self.usernames.append(username)

    def getSearchResultsFor(self, searchString):
        results = []
        for username in self.usernames:
            if searchString in username:
                results.append(username)
        return sorted(results)
