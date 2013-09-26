from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class NestedElementsTest(ConcordionTestCase):
    def matchOrNotMatch(self, snippet, outcome):
        t = TestRig()
        t.stub_result(outcome)
        result = t.process_fragment(snippet)
        return "match" if not result.has_failed() else "not match"
