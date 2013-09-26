from base import ConcordionTestCase
from test_rig import TestRig


class EchoTest(ConcordionTestCase):
    nextResult = None

    def setNextResult(self, result):
        self.nextResult = result

    def render(self, fragment):
        rig = TestRig()
        rig.stub_result(self.nextResult)
        rig.process_fragment(fragment)
        return rig.get_output_fragment_xml()
