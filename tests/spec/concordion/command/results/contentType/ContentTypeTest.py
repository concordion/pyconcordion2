from __future__ import unicode_literals

from lxml import etree

from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig


class ContentTypeTest(ConcordionTestCase):
    def process(self, html):
        result = TestRig().process_html(html)
        # self.removeIrrelevantElements(result.root_element)
        return etree.tostring(result.root_element)

    def removeIrrelevantElements(self, root_element):
        self.removeIrrelevantStylesheet(root_element)
        self.removeIrrelevantFooter(root_element)

    def removeIrrelevantStylesheet(self, root_element):
        head = root_element.xpath("//head")[0]
        style = head.xpath("//style")[0]
        head.remove(style)

    def removeIrrelevantFooter(self, root_element):
        body = root_element.xpath("//body")
        body.remove(root_element.xpath("//div[@class='footer']")[0])
