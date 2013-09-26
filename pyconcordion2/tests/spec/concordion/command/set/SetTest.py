from base import ConcordionTestCase
from test_rig import TestRig


class SetTest(ConcordionTestCase):
    param = None

    def process(self, snippet):
        t = TestRig(self)
        return t.process_fragment(snippet)

    def getParameterPassedIn(self):
        return self.param

    def setUpUser(self, full_name):
        self.param = full_name
