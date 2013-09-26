from __future__ import unicode_literals

from base import ConcordionTestCase
from test_rig import TestRig


class VerifyRowsTest(ConcordionTestCase):
    _usernames = []

    def processFragment(self, fragment, csv):
        self._usernames = [username.strip() for username in csv.split(",")]
        result = TestRig(fixture=self).process_fragment(fragment)
        return self.categorize(result)

    def categorize(self, result):
        css_classes = []
        table = result.root_element.xpath("//table")[0]
        for row in table.xpath(".//tr"):
            css_class = row.attrib.get("class")
            if not css_class:
                try:
                    cell = row.xpath("td")[0]
                except:
                    continue
                css_class = cell.attrib.get("class")
            if css_class:
                css_classes.append(css_class.upper())
        return ", ".join(css_classes)

    def usernames(self):
        return self._usernames