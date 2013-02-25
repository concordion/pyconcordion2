from __future__ import unicode_literals
from collections import OrderedDict
import os
import tempfile
import unittest

from lxml import etree

from commands import command_mapper


TEMP_DIR = tempfile.gettempdir()
CONCORDION_NAMESPACE = "http://www.concordion.org/2007/concordion"


class ConcordionTestCase(unittest.TestCase):
    def test_fixture(self):
        filename = self.__find_spec()
        self.__build_command_tree(filename)

    def __find_parent(self, tree, command):
        element = command.element
        while element.getparent() is not None:
            if element.getparent() in tree:
                tree[element.getparent()].children.append(command)
                return True
            else:
                element = element.getparent()
        return False

    def __find_spec(self):
        filename = self.__class__.__name__
        if filename[-4:].lower() == "test":
            filename = filename[:-4]
        filename, ext = os.path.splitext(os.path.realpath(filename))
        filename += ".html"
        with open(filename): # will raise exception if it doesn't exist
            return filename

    def __build_command_tree(self, filename):
        self.args = {}
        tree = etree.parse(filename)
        elements = tree.xpath("""//*[namespace-uri()='{namespace}' or @*[namespace-uri()='{namespace}']]""".format(
            namespace=CONCORDION_NAMESPACE))

        commands = OrderedDict()

        for element in elements:
            for key, expression_str in element.attrib.items():
                if CONCORDION_NAMESPACE not in key:
                    continue

                key = key.replace("{%s}" % CONCORDION_NAMESPACE, "")

                command_cls = command_mapper.get(key)
                command = command_cls(element, expression_str, self)
                if not self.__find_parent(commands, command):
                    commands[command.element] = command

        for element, command in commands.items():
            command.run()

        self.__write(filename, tree)

    def __write(self, filename, tree):
        css_path = os.path.join(os.path.dirname(__file__), "..", "resources", "css", "embedded.css")
        try:
            css = open(css_path, "rU").read()
        except:
            css = ""

        with open(os.path.join(TEMP_DIR, os.path.basename(filename)), "w") as f:
            print "Saving to:\n%s" % f.name
            css_tag = etree.Element("style")
            css_tag.attrib["type"] = "text/css"
            css_tag.text = css

            tree.getroot().insert(0, css_tag)
            f.write(etree.tostring(tree))

        if tree.xpath("//@class='failure'") or tree.xpath("//@class='missing'"):
            raise AssertionError("Test failed")
