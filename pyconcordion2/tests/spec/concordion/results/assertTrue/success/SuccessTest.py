from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class SuccessTest(ConcordionTestCase):
    def isPalindrome(self, s):
        return s == s[::-1]

    def render(self, fragment):
        rig = TestRig(fixture=self)
        rig.process_fragment(fragment)
        return rig.get_output_fragment_xml()
