from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class ExceptionsTest(ConcordionTestCase):
    def countsFromExecutingSnippetWithSimulatedEvaluationResult(self, snippet, outcome):
        t = TestRig()
        if outcome == "(An exception)":
            t.stub_result(RuntimeError())
        else:
            t.stub_result(outcome)
        return t.process_fragment(snippet)
