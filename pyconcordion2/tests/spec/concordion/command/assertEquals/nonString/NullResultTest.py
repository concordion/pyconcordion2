from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class NullResultTest(ConcordionTestCase):
    def outcomeOfPerformingAssertEquals(self, fragment, expectedString, result):
        if result == "None":
            result = None

        fragment = fragment.replace("(some expectation)", expectedString)

        t = TestRig()
        t.stub_result(result)
        t.process_fragment(fragment)
        return t.success_or_failure()
