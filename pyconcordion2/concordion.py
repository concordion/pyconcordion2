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
        output_dir = os.path.join(TEMP_DIR, self.extra_folder)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, os.path.basename(filename)), "w") as f:
            print "Saving to:\n%s" % f.name
            f.write(etree.tostring(tree, pretty_print=True))
