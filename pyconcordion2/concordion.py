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
        css_path = os.path.join(os.path.dirname(__file__), "resources", "css", "embedded.css")
        jquery_path = os.path.join(os.path.dirname(__file__), "resources", "js", "jquery-1.9.1.min.js")
        js_path = os.path.join(os.path.dirname(__file__), "resources", "js", "main.js")

        with open(os.path.join(TEMP_DIR, os.path.basename(filename)), "w") as f:
            print "Saving to:\n%s" % f.name
            css_tag = etree.Element("link", rel="stylesheet", href=css_path)

            js_tag = etree.Element("script", src=js_path)
            js_tag.text = " "
            jquery_tag = etree.Element("script", src=jquery_path)
            jquery_tag.text = " "

            tree.getroot().insert(0, css_tag)
            tree.getroot().append(jquery_tag)
            tree.getroot().append(js_tag)
            f.write(etree.tostring(tree, pretty_print=True))

    def __report_test_summary(self, tree):
        if (tree.xpath("//@class='failure'") or tree.xpath("//@class='missing'") or
                tree.xpath("//@class='exceptionMessage'")):
            raise AssertionError("Test failed")
