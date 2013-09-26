from base import ConcordionTestCase
from test_rig import TestRig


class EscapingHtmlCharactersTest(ConcordionTestCase):
    def render(self, fragment, evalResult):
        rig = TestRig()
        rig.stub_result(evalResult)
        rig.process_fragment(fragment)
        result = rig.get_output_fragment_xml()
        return result.replace(" concordion:echo=\"username\">", ">")
