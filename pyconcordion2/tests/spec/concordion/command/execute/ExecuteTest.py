from base import ConcordionTestCase
from test_rig import TestRig


class ExecuteTest(ConcordionTestCase):
    method_called = False

    def myMethodWasCalledProcessing(self, fragment):
        t = TestRig(fixture=self)
        t.process_fragment(fragment)
        return "Will" if self.method_called else "Will Not"

    def myMethod(self):
        self.method_called = True
