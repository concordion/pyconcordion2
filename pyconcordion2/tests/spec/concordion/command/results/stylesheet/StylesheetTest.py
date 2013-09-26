from __future__ import unicode_literals

from lxml import etree

from base import ConcordionTestCase
from test_rig import TestRig


class StylesheetTest(ConcordionTestCase):
    def processDocument(self, html):
        self.rig = TestRig()
        result = self.rig.process_html(html)
        self.root_element = result.root_element

    def getRelativePosition(self, outer, target, sibling):
        outer_tag = self.root_element.xpath("//{}".format(outer))[0]

        target_index = 0
        sibling_index = 0
        for i, children in enumerate(outer_tag.getchildren()):
            if children.tag == target:
                target_index = i
            elif children.tag == sibling:
                sibling_index = i

        return "after" if target_index > sibling_index else "before"

    def elementTextContains(self, elementName, s1, s2):
        element_tag = self.root_element.xpath("//{}".format(elementName))[0]

        element_text = etree.tostring(element_tag)
        result = s1 in element_text and s2 in element_text
        return "should" if result else "should not"
