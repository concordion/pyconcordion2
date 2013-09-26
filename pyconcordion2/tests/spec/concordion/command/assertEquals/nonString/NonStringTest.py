from __future__ import unicode_literals
from base import ConcordionTestCase
from test_rig import TestRig


class NonStringTest(ConcordionTestCase):
    def outcomeOfPerformingAssertEquals(self, fragment, expectedString, result, resultType):

        if resultType == "String":
            simulatedResult = result
        elif resultType == "Integer":
            simulatedResult = int(result)
        elif resultType == "Double":
            simulatedResult = float(result)
        else:
            raise RuntimeError("Unsupported result-type '{}'".format(resultType ))

        fragment = fragment.replace("(some expectation)", expectedString)

        t = TestRig()
        t.stub_result(simulatedResult)
        t.process_fragment(fragment)
        return t.success_or_failure()
