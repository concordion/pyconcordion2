from __future__ import unicode_literals
import inspect
import logging
import os
import sys
import tempfile
import unittest

from lxml import etree

from commands import Commander

logger = logging.getLogger(__file__)
logger.level = logging.INFO

TEMP_DIR = tempfile.gettempdir()


class ConcordionTestCase(unittest.TestCase):
    extra_folder = "."

    stream_handler = logging.StreamHandler(sys.stdout)

    @classmethod
    def setUpClass(cls):
        logger.addHandler(cls.stream_handler)

    @classmethod
    def tearDownClass(cls):
        logger.removeHandler(cls.stream_handler)

    def runTest(self):
        # hack to prevent the base class to be run
        if self.__class__.__name__ == ConcordionTestCase.__name__:
            return True

        filename = self._find_spec()

        runner = Commander(self, filename)
        runner.process()

        runner.tree.xpath("//body")[0].insert(0, self.bread_crumb_tag())
        self.__write(filename, runner.tree)
        self.assertTrue(runner.result.has_succeeded())

    def _find_spec(self):
        """
        We find the filename of the spec based on the name of the test. If the class ends in "test" we remove it.
        """
        filename, ext = os.path.splitext(inspect.getfile(self.__class__))
        if filename[-4:].lower() == "test":
            filename = filename[:-4]
        filename += ".html"
        with open(filename):  # will raise exception if it doesn't exist
            return filename

    def bread_crumbs(self):
        head, tail = os.path.split(self.file_path())
        crumbs = []
        while True:
            head, tail = os.path.split(head)

            # we do this because capitalize() makes the first character uppercase and everything else lowercase
            base = os.path.join(head, tail, tail[0].upper() + tail[1:])

            crumb = base + ".html"
            # we skip if we're looking at the current spec
            if crumb == self._find_spec():
                continue
            if os.path.exists(crumb):
                crumbs.append(crumb)
            else:
                break
        return reversed(crumbs)

    def bread_crumb_tag(self):
        span_tag = etree.Element("span", {"class": "breadcrumbs"})
        for crumb in self.bread_crumbs():
            crumb_relpath = os.path.relpath(crumb, os.path.dirname(self.file_path()))
            a_tag = etree.Element("a", href=crumb_relpath)
            a_tag.text = os.path.splitext(os.path.basename(crumb_relpath))[0]
            a_tag.tail = " > "
            span_tag.append(a_tag)
        return span_tag

    def __write(self, filename, tree):
        output_dir = os.getenv('PYCONCORDION_OUTPUT', TEMP_DIR)
        output_dir = os.path.join(output_dir, self.extra_folder)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, os.path.basename(filename)), "w") as f:
            logger.info("Saving to:\n%s" % f.name)
            f.write(etree.tostring(tree, pretty_print=True))

    def file_path(self):
        return os.path.abspath(inspect.getfile(self.__class__))
