from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class Result(object):
    def __init__(self):
        self._successes = []
        self._failures = []

    @property
    def successes(self):
        return ", ".join(self._successes)

    @property
    def failures(self):
        return ", ".join(self._failures)


class LineContinuationsTest(ConcordionTestCase):
    def setUp(self):
        self.snippets = []

    def addSnippet(self, snippet):
        self.snippets.append(snippet)

    def processSnippets(self, evaluationResult):
        result = Result()

        for i, snippet in enumerate(self.snippets, start=1):
            t = TestRig()
            t.stub_result(evaluationResult)
            has_failed = t.process_fragment(snippet).has_failed()

            if has_failed:
                result._failures.append("({})".format(i))
            else:
                result._successes.append("({})".format(i))
        return result
