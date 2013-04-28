import unittest
from case import ConcordionTestCase


class AccessToLinkHrefTest(ConcordionTestCase):
    @unittest.expectedFailure
    def runTest(self):
        super(AccessToLinkHrefTest, self).runTest()
