from __future__ import unicode_literals
from collections import namedtuple

from pyconcordion2 import ConcordionTestCase

Person = namedtuple("Person", ["firstName", "lastName"])


class SpikeTest(ConcordionTestCase):
    def getGreetingFor(self, name):
        return "Hello %s!" % name

    def doSomething(self):
        pass

    def getPeople(self):
        1/0
        return [Person("John", "Travolta"), Person("Frank", "Zappa")]
