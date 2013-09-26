from __future__ import unicode_literals
from collections import OrderedDict
from io import BytesIO
from operator import attrgetter
import imp
import inspect
import itertools
import os
import re
import traceback
import unittest

from enum import Enum
from lxml import etree
from lxml import html

import expression_parser

truth_values = ['true', '1', 't', 'y', 'yes']

CHAR_SPACE = '\u00A0'

CONCORDION_NAMESPACE = "http://www.concordion.org/2007/concordion"


class Status(Enum):
    success = 1
    failure = 2
    ignored = 3


class ResultEvent(object):
    def __init__(self, actual, expected):
        self.actual = actual
        self.expected = expected


class Result(object):
    def __init__(self, tree):
        self.root_element = tree
        self.successes = tree.xpath("//*[contains(concat(' ', @class, ' '), ' success ')]")
        self.failures = tree.xpath("//*[contains(concat(' ', @class, ' '), ' failure ')]")
        self.missing = tree.xpath("//*[contains(concat(' ', @class, ' '), ' missing ')]")
        self.exceptions = tree.xpath("//*[contains(concat(' ', @class, ' '), ' exceptionMessage ')]")

    def last_failed_event(self):
        last_failed = self.failures[-1]
        actual = last_failed.xpath("//*[@class='actual']")[0].text
        expected = last_failed.xpath("//*[@class='expected']")[0].text
        return ResultEvent(actual, expected)

    @property
    def num_failure(self):
        return len(self.failures)

    @property
    def num_exception(self):
        return len(self.exceptions)

    @property
    def num_missing(self):
        return len(self.missing)

    @property
    def num_success(self):
        return len(self.successes)

    def has_failed(self):
        return bool(self.num_failure or self.num_exception or self.num_missing)

    def has_succeeded(self):
        return not self.has_failed()


class Commander(object):
    def __init__(self, test, filename):
        self.test = test
        self.filename = filename
        self.tree = etree.parse(self.filename)
        self.args = {}
        self.commands = OrderedDict()

    def process(self):
        """
        1. Finds all concordion elements
        2. Iterates over concordion attributes
        3. Generates ordered dictionary of commands
        4. Executes commands in order
        """
        elements = self.__find_concordion_elements()

        for element in elements:
            for key, expression_str in element.attrib.items():
                if CONCORDION_NAMESPACE not in key:  # we ignore any attributes that are not concordion
                    continue

                key = key.replace("{%s}" % CONCORDION_NAMESPACE, "")  # we remove the namespace

                command_cls = command_mapper.get(key)
                command = command_cls(element, expression_str, self.test)

                if element.tag.lower() == "th":
                    index = self.__find_th_index(element)
                    command.index = index

                self.__add_to_commands_dict(command)

        self.__run_commands()
        self.__postprocess_tree()
        self.result = Result(self.tree)

    def __find_concordion_elements(self):
        """
        Retrieves all etree elements with the concordion namespace
        """
        return self.tree.xpath("""//*[namespace-uri()='{namespace}' or @*[namespace-uri()='{namespace}']]""".format(
            namespace=CONCORDION_NAMESPACE))

    def __find_th_index(self, element):
        """
        Returns the index of the given table header cell
        """
        parent = element.getparent()
        for index, th_element in enumerate(parent.xpath("th")):
            if th_element == element:
                return index
        raise RuntimeError("Could not match command with table header")  # should NEVER happen

    def __add_to_commands_dict(self, command):
        """
        Given a command, we check to see if it's a child of another command. If it is we add it to the list of child
        commands. Otherwise we set it as a brand new command
        """
        element = command.element
        while element.getparent() is not None:
            if element.getparent() in self.commands:
                self.commands[element.getparent()].children.append(command)
                return
            else:
                element = element.getparent()
        self.commands[command.element] = command

    def __run_commands(self):
        """
        Runs each command in order
        """
        for element, command in self.commands.items():
            command.run()

    def __postprocess_tree(self):
        css_path = os.path.join(os.path.dirname(__file__), "resources", "embedded.css")
        css_contents = open(css_path, "rU").read()

        js_path = os.path.join(os.path.dirname(__file__), "resources", "main.js")
        js_contents = open(js_path, "rU").read()

        meta = etree.Element("meta")
        meta.attrib["http-equiv"] = "content-type"
        meta.attrib["content"] = "text/html; charset=UTF-8"
        meta.tail = "\n"

        head = self.tree.xpath("//head")
        if head:
            head[0].insert(0, meta)
        else:
            head = etree.Element("head")
            head.text = "\n"
            head.append(meta)

            for child in self.tree.getroot().getchildren():
                if child.tag == "body":
                    break
                head.append(child)
            head.tail = "\n"

            self.tree.getroot().insert(0, head)

        head = self.tree.xpath("//head")[0]
        style_tag = etree.Element("style", type="text/css")
        style_tag.text = css_contents
        head.insert(0, style_tag)

        js_tag = etree.Element("script")
        js_tag.text = js_contents
        jquery_tag = etree.Element("script", src="http://code.jquery.com/jquery-1.10.2.min.js")
        jquery_tag.text = " "

        self.tree.getroot().append(jquery_tag)
        self.tree.getroot().append(js_tag)


class Command(object):
    def __init__(self, element, expression_str, context):
        self.element = element
        self.expression_str = expression_str.replace("#", "")
        self.context = context
        self.children = []

    def _run(self):
        raise NotImplementedError

    def run(self):
        try:
            self.context.TEXT = get_element_content(self.element)
            self._run()
            return True
        except Exception as e:
            mark_exception(self.element, e)


class RunCommand(Command):
    def _run(self):
        href = self.element.attrib["href"].replace(".html", "")
        f = inspect.getfile(self.context.__class__)
        file_path = os.path.join(os.path.dirname(os.path.abspath(f)), href)

        if os.path.exists(file_path + ".py"):
            src_file_path = file_path + ".py"
        elif os.path.exists(file_path + "Test.py"):
            src_file_path = file_path + "Test.py"
        else:
            raise RuntimeError("Cannot find Python Test file")

        modname, ext = os.path.splitext(os.path.basename(src_file_path))
        test_class = imp.load_source(modname, src_file_path)

        test_class = getattr(test_class, modname)()
        test_class.extra_folder = os.path.dirname(os.path.join(self.context.extra_folder, href))
        result = unittest.TextTestRunner().run(test_class)
        if result.failures or result.errors:
            mark_status(Status.failure, self.element)
        elif result.expectedFailures:
            mark_status(Status.ignored, self.element)
        else:
            mark_status(Status.success, self.element)


class ExecuteCommand(Command):
    def _run(self):
        if self.element.tag.lower() == "table":
            for row in get_table_body_rows(self.element):
                for command in self.children:
                    td_element = row.xpath("td")[command.index]
                    command.element = td_element
                self._run_children()
        else:
            self._run_children()

    def _run_children(self):
        for command in self.children:
            if isinstance(command, SetCommand):
                command.run()
        expression_parser.execute_within_context(self.context, self.expression_str)
        for command in self.children:
            if not isinstance(command, SetCommand):
                command.run()


class VerifyRowsCommand(Command):
    def _run(self):
        variable_name = expression_parser.parse(self.expression_str).variable_name
        results = expression_parser.execute_within_context(self.context, self.expression_str)
        for result, row in itertools.izip_longest(results, get_table_body_rows(self.element)):
            setattr(self.context, variable_name, result)

            if result is None:
                row.attrib["class"] = (row.attrib.get("class", "") + " missing").strip()
                continue

            if row is None:
                total_columns = max(self.children, key=attrgetter("index")).index + 1  # good enough but not perfect
                row = etree.Element("tr", **{"class": "surplus"})
                for _ in xrange(total_columns):
                    etree.SubElement(row, "td")
                if self.element.xpath("//tbody"):
                    self.element.xpath("//tbody")[0].append(row)
                else:
                    self.element.append(row)

            for command in self.children:
                element = row.xpath("td")[command.index]
                command.element = element
                command.run()


def get_table_body_rows(table):
    if table.xpath("//tbody"):
        tr_s = table.xpath("//tbody/tr")
    else:
        tr_s = table.xpath("tr")
    return [tr for tr in tr_s if tr.xpath("td")]


def normalize(text):
    text = unicode(text)
    text = text.replace(" _\n", "")  # support for python style line breaks
    pattern = re.compile(r'\s+')  # treat all whitespace as spaces
    return re.sub(pattern, ' ', text).strip()


def get_element_content(element):
    tag_html = html.parse(BytesIO(etree.tostring(element))).getroot().getchildren()[0].getchildren()[0]
    return normalize(tag_html.text_content())


class SetCommand(Command):
    def _run(self):
        expression = expression_parser.parse(self.expression_str)
        if expression.function_name:  # concordion:set="blah = function(#TEXT)"
            expression_parser.execute_within_context(self.context, self.expression_str)
        else:
            setattr(self.context, expression.variable_name, get_element_content(self.element))


class AssertEqualsCommand(Command):
    def _run(self):
        expression_return = expression_parser.execute_within_context(self.context, self.expression_str)
        if expression_return is None:
            expression_return = "(None)"

        result = normalize(expression_return) == get_element_content(self.element)
        if result:
            mark_status(Status.success, self.element)
        else:
            mark_status(Status.failure, self.element, expression_return)


class AssertTrueCommand(Command):
    def _run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        if result:
            mark_status(Status.success, self.element)
        else:
            mark_status(Status.failure, self.element, "== false")


class AssertFalseCommand(Command):
    def _run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        if not result:
            mark_status(Status.success, self.element)
        else:
            mark_status(Status.failure, self.element, "== true")


class EchoCommand(Command):
    def _run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        if result is not None:
            self.element.text = result
        else:
            em = etree.Element("em")
            em.text = "None"
            self.element.append(em)


def mark_status(status, element, actual_value=None):
    if not get_element_content(element):  # set non-breaking space if element is empty
        element.text = CHAR_SPACE

    element.attrib["class"] = (element.attrib.get("class", "") + " {}".format(status.name)).strip()
    if actual_value is not None:
        actual = etree.Element("ins", **{"class": "actual"})
        actual.text = unicode(actual_value) or CHAR_SPACE  # blank space if no value

        # we move child elements from element into our new del container
        expected = etree.Element("del", **{"class": "expected"})
        for child in element.getchildren():
            expected.append(child)
        expected.text = element.text
        element.text = None
        expected.tail = "\n"

        element.insert(0, expected)
        element.insert(1, actual)


__exception_index = 1


def mark_exception(target_element, e):
    global __exception_index
    exception_element = etree.Element("span", **{"class": "exceptionMessage"})
    exception_element.text = unicode(e)

    input_element = etree.Element("input",
                                  **{"class": "stackTraceButton", "data-exception-index": unicode(__exception_index),
                                     "type": "button", "value": "Toggle Stack"})

    stacktrace_div_element = etree.Element("div", **{"class": "stackTrace {}".format(__exception_index)})
    p_tag = etree.Element("p")
    p_tag.text = "Traceback:"
    stacktrace_div_element.append(p_tag)
    tb = traceback.format_exc()
    for line in tb.splitlines():
        trace_element = etree.Element("div", **{"class": "stackTraceEntry"})
        trace_element.text = line
        stacktrace_div_element.append(trace_element)

    parent = target_element.getparent()
    # we insert the exception after the element in question
    for i, element in enumerate((exception_element, input_element, stacktrace_div_element)):
        parent.insert(parent.index(target_element) + 1 + i, element)

    __exception_index += 1


command_mapper = {
    "run": RunCommand,
    "execute": ExecuteCommand,
    "set": SetCommand,
    "assertEquals": AssertEqualsCommand,
    "assertTrue": AssertTrueCommand,
    "assertFalse": AssertFalseCommand,
    "verifyRows": VerifyRowsCommand,
    "echo": EchoCommand
}
