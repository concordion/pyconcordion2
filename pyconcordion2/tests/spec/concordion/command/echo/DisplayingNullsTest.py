from base import ConcordionTestCase
from test_rig import TestRig


class DisplayingNullsTest(ConcordionTestCase):
    def render(self, fragment):
        rig = TestRig()
        rig.stub_result(None)
        rig.process_fragment(fragment)
        result = rig.get_output_fragment_xml()
        return result.replace(" concordion:echo=\"username\">", ">")
