from concordion import ConcordionTestCase


class PartialMatches(ConcordionTestCase):
    usernames = []

    def setUpUser(self, username):
        self.usernames.append(username)

    def getSearchResultsFor(self, searchString):
        results = []
        for username in self.usernames:
            if searchString in username:
                results.append(username)
        return sorted(results)