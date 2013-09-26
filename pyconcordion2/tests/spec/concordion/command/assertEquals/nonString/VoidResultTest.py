from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class VoidResultTest(ConcordionTestCase):
    def process(self, fragment):
        t = TestRig(fixture=self)
        t.stub_result(None)
        t.process_fragment(fragment)
        return t.success_or_failure()

    def myVoidMethod(self):
        pass
