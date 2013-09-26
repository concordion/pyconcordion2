from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig, text_to_bool


class AssertTrueTest(ConcordionTestCase):
    def successOrFailure(self, snippet, outcome):
        t = TestRig()
        t.stub_result(text_to_bool(outcome))
        t.process_fragment(snippet)
        return t.success_or_failure()
