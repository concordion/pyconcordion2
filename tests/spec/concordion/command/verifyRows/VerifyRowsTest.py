from __future__ import unicode_literals

from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig


class VerifyRowsTest(ConcordionTestCase):
    _usernames = []

    def processFragment(self, fragment, csv):
        self._usernames = [username.strip() for username in csv.split(",")]
        result = TestRig(fixture=self).process_fragment(fragment)
        return result.has_failed()

    def usernames(self):
        return self._usernames