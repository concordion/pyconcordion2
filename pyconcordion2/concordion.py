from __future__ import unicode_literals
import inspect
import os
import tempfile
import unittest

from lxml import etree

from commands import Commander


TEMP_DIR = tempfile.gettempdir()


class ConcordionTestCase(unittest.TestCase):
    extra_folder = "."

    def runTest(self):
        # hack to prevent the base class to be run
        if self.__class__.__name__ == ConcordionTestCase.__name__:
            return True

        filename = self.__find_spec()

        runner = Commander(self, filename)
        runner.process()
        self.__write(filename, runner.tree)
        self.assertTrue(runner.result.has_succeeded())

    def __find_spec(self):
        """
        We find the filename of the spec based on the name of the test. If the class ends in "test" we remove it.
        """
        filename, ext = os.path.splitext(inspect.getfile(self.__class__))
        if filename[-4:].lower() == "test":
            filename = filename[:-4]
        filename += ".html"
        with open(filename):  # will raise exception if it doesn't exist
            return filename

    def __write(self, filename, tree):
        css_path = os.path.join(os.path.dirname(__file__), "resources", "css", "embedded.css")
        jquery_path = os.path.join(os.path.dirname(__file__), "resources", "js", "jquery-1.9.1.min.js")
        js_path = os.path.join(os.path.dirname(__file__), "resources", "js", "main.js")

        output_dir = os.path.join(TEMP_DIR, self.extra_folder)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, os.path.basename(filename)), "w") as f:
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
