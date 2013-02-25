from __future__ import unicode_literals

from concordion import ConcordionTestCase

class DemoTest(ConcordionTestCase):
    def greetingFor(self, firstName):
        return "Hello %s!" % firstName
