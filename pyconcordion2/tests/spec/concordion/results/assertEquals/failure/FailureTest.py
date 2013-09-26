from __future__ import unicode_literals

from base import ConcordionTestCase
from test_rig import TestRig


class FailureTest(ConcordionTestCase):
    def setUp(self):
        self.acronym = None

    def renderAsFailure(self, fragment, acronym):
        self.acronym = acronym
        test_rig = TestRig(fixture=self)
        test_rig.process_fragment(fragment)
        return test_rig.get_output_fragment_xml()
