from __future__ import unicode_literals

from lxml import etree

from base import ConcordionTestCase
from test_rig import TestRig


class ContentTypeTest(ConcordionTestCase):
    def process(self, html):
        result = TestRig().process_html(html)
        self.remove_irrelevant_elements(result.root_element)
        return etree.tostring(result.root_element)

    def remove_irrelevant_elements(self, root_element):
        self.remove_irrelevant_stylesheet(root_element)
        self.remove_script_elements(root_element)

    def remove_script_elements(self, root_element):
        for script in root_element.xpath("//script"):
            script.getparent().remove(script)

    def remove_irrelevant_stylesheet(self, root_element):
        head = root_element.xpath("//head")[0]
        style = head.xpath("//style")[0]
        head.remove(style)
