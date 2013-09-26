from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class SupportedElementsTest(ConcordionTestCase):
    def process(self, snippet):
        t = TestRig()
        t.stub_result("Fred")
        result = t.process_fragment(snippet)
        return snippet if not result.has_failed() else "Did not work"
