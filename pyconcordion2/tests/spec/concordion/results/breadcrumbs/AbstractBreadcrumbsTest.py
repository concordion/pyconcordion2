from __future__ import unicode_literals
from lxml import etree
from pyconcordion2 import ConcordionTestCase
from test_rig import TestRig


class Result(object):
    def __init__(self):
        self.text = ""
        self.html = ""


class AbstractBreadcrumbsTest(ConcordionTestCase):
    def setUp(self):
        self.test_rig = TestRig()

    # def setUpResource(self, resourceName, content):
    #     self.test_rig.withResource(Resource(resourceName), content)
    #
    # def getBreadcrumbsFor(self, resourceName):
    #     result = self.test_rig.process(Resource(resourceName))
    #     span_elements = result.root_element.xpath("//span")
    #
    #     result = Result()
    #     for span in span_elements:
    #         if "breadcrumbs" == span.attrib.get("class"):
    #             result.html = etree.tostring(span)
    #             result.text = span.text
    #     return result
#