from __future__ import unicode_literals
from concordion import ConcordionTestCase


class Person(object):
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName


class Spike(ConcordionTestCase):
    def getGreetingFor(self, name):
        return "Hello %s!" % name

    def doSomething(self):
        pass

    def getPeople(self):
        return [Person("John", "Travolta"), Person("Frank", "Zappa")]
