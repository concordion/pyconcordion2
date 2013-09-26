from __future__ import unicode_literals
import unittest
from case import ConcordionTestCase


class ExtensionTest(ConcordionTestCase):
    @unittest.expectedFailure
    def runTest(self):
        super(ExtensionTest, self).runTest()