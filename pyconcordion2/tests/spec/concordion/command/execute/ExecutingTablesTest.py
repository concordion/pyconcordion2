from base import ConcordionTestCase
from test_rig import TestRig


class ExecutingTablesTest(ConcordionTestCase):
    def process(self, fragment):
        r = TestRig(fixture=self).process_fragment(fragment)

        result = Result()
        result.successCount = r.num_success
        result.failureCount = r.num_failure
        result.exceptionCount = r.num_exception

        lastEvent = r.last_failed_event()
        if lastEvent is not None:
            result.lastActualValue = lastEvent.actual
            result.lastExpectedValue = lastEvent.expected

        return result

    def generateUsername(self, fullName):
        return fullName.replace(" ", "").lower()


class Result(object):
    successCount = None
    failureCount = None
    exceptionCount = None
    lastExpectedValue = None
    lastActualValue = None
