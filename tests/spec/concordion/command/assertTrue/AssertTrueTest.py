from __future__ import unicode_literals
from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig, text_to_bool


class AssertTrueTest(ConcordionTestCase):
    def successOrFailure(self, snippet, outcome):
        t = TestRig()
        t.stub_result(text_to_bool(outcome))
        return "SUCCESS" if t.process_fragment(snippet) else "FAILURE"
