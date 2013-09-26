from __future__ import unicode_literals

from base import ConcordionTestCase
from test_rig import TestRig


class ExampleTest(ConcordionTestCase):
    def process(self, html):
        result = TestRig(fixture=self).process_html(html)
        return "success" if result.has_succeeded() else "failure"

    def greeting(self):
        return "Hello World!"
