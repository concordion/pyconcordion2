from __future__ import unicode_literals
from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig


class AssertEqualsTest(ConcordionTestCase):
    def successOrFailure(self, snippet, outcome):
        t = TestRig()
        t.stub_result(outcome)
        t.process_fragment(snippet)
        return t.success_or_failure()
