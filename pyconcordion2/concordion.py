from __future__ import unicode_literals
import os
import tempfile
import unittest

from lxml import etree

from commands import Commander


TEMP_DIR = tempfile.gettempdir()


class ConcordionTestCase(unittest.TestCase):
    def test_fixture(self):
        filename = self.__find_spec()

        runner = Commander(self, filename)
        runner.process()
        self.__write(filename, runner.tree)
        self.__report_test_summary(runner.tree)

    def __find_spec(self):
        """
        We find the filename of the spec based on the name of the test. If the class ends in "test" we remove it.
        """
        filename = self.__class__.__name__
        if filename[-4:].lower() == "test":
            filename = filename[:-4]
        filename, ext = os.path.splitext(os.path.realpath(filename))
        filename += ".html"
        with open(filename):  # will raise exception if it doesn't exist
            return filename

    def __write(self, filename, tree):
        css_path = os.path.join(os.path.dirname(__file__), "..", "resources", "css", "embedded.css")
        try:
            css = open(css_path, "rU").read()
        except:
            css = ""

        with open(os.path.join(TEMP_DIR, os.path.basename(filename)), "w") as f:
            print "Saving to:\n%s" % f.name
            css_tag = etree.Element("style", type="text/css")
            css_tag.text = css

            tree.getroot().insert(0, css_tag)
            f.write(etree.tostring(tree))

    def __report_test_summary(self, tree):
        if tree.xpath("//@class='failure'") or tree.xpath("//@class='missing'"):
            raise AssertionError("Test failed")
