from __future__ import unicode_literals

from pyconcordion2 import ConcordionTestCase


class Person(object):
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName


class SpikeTest(ConcordionTestCase):
    def getGreetingFor(self, name):
        return "Hello %s!" % name

    def doSomething(self):
        pass

    def getPeople(self):
        return [Person("John", "Travolta"), Person("Frank", "Zappa")]
