from __future__ import unicode_literals
import unittest
from base import ConcordionTestCase


class ExtensionTest(ConcordionTestCase):
    @unittest.expectedFailure
    def runTest(self):
        super(ExtensionTest, self).runTest()