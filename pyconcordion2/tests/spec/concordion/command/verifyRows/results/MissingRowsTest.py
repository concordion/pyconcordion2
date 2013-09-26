from __future__ import unicode_literals

from base import ConcordionTestCase
from test_rig import TestRig


class MissingRowsTest(ConcordionTestCase):
    def setUp(self):
        self.people = []

    def addPerson(self, firstName, lastName, birthYear):
        self.people.append(Person(firstName, lastName, birthYear))

    def getOutputFragment(self, inputFragment):
        test_rig = TestRig(fixture=self)
        test_rig.process_fragment(inputFragment)
        return test_rig.get_output_fragment_xml()

    def getPeople(self):
        return self.people


class Person(object):
    def __init__(self, firstName, lastName, birthYear):
        self.firstName = firstName
        self.lastName = lastName
        self.birthYear = birthYear
