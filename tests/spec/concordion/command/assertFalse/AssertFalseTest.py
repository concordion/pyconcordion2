from __future__ import unicode_literals
from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig
from test_rig import text_to_bool


class AssertFalseTest(ConcordionTestCase):
    def successOrFailure(self, snippet, outcome):
        t = TestRig()
        t.stub_result(text_to_bool(outcome))
        return "SUCCESS" if t.process_fragment(snippet) else "FAILURE"