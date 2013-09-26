from __future__ import unicode_literals
from collections import namedtuple

from base import ConcordionTestCase

Person = namedtuple("Person", ["firstName", "lastName"])


class SpikeTest(ConcordionTestCase):
    def getGreetingFor(self, name):
        return "Hello %s!" % name

    def doSomething(self, text):
        pass

    def getPeople(self):
        return [Person("John", "Travolta"), Person("Frank", "Zappa")]
