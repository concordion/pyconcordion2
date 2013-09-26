from __future__ import unicode_literals

from base import ConcordionTestCase
from test_rig import TestRig


class TableBodySupportTest(ConcordionTestCase):
    def setUp(self):
        self.names = []

    def setUpNames(self, namesAsCSV):
        self.names = namesAsCSV.split(", ")

    def getNames(self):
        return self.names

    def process(self, inputFragment):
        test_rig = TestRig(fixture=self)
        test_rig.process_fragment(inputFragment)
        return test_rig.get_output_fragment_xml()
