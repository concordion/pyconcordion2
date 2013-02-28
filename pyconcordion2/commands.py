from __future__ import unicode_literals
from collections import OrderedDict
import traceback

from lxml import etree

import expression_parser


CONCORDION_NAMESPACE = "http://www.concordion.org/2007/concordion"


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

    def __find_concordion_elements(self):
        """
        Retrieves all etree elements with the concordion namespace
        """
        return self.tree.xpath("""//*[namespace-uri()='{namespace}' or @*[namespace-uri()='{namespace}']]""".format(
            namespace=CONCORDION_NAMESPACE))

    def __find_th_index(self, element):
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
            self._run()
        except Exception as e:
            mark_exception(self.element, e)


class RunCommand(Command):
    pass


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
        for result, row in zip(results, get_table_body_rows(self.element)):
            setattr(self.context, variable_name, result)
            for command in self.children:
                element = row.xpath("td")[command.index]
                command.element = element
                command.run()


def get_table_body_rows(table):
    tr_s = table.xpath("tr")
    return [tr for tr in tr_s if tr.xpath("td")]


class SetCommand(Command):
    def _run(self):
        expression = expression_parser.parse(self.expression_str)
        assert expression.variable_name
        setattr(self.context, self.expression_str, self.element.text)


class AssertEqualsCommand(Command):
    def _run(self):
        expression_return = expression_parser.execute_within_context(self.context, self.expression_str)
        result = unicode(expression_return) == unicode(self.element.text)
        if result:
            mark_status(result, self.element)
        else:
            mark_status(result, self.element, expression_return)


class AssertTrueCommand(Command):
    def _run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        mark_status(result, self.element)


class AssertFalseCommand(Command):
    def _run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        mark_status(not result, self.element)


class EchoCommand(Command):
    def _run(self):
        return expression_parser.execute_within_context(self.context, self.expression_str)


def mark_status(is_successful, element, actual_value=None):
    if is_successful:
        element.attrib["class"] = "success"
    else:
        element.attrib["class"] = "failure"

    if actual_value:
        actual = etree.Element("ins", **{"class": "actual"})
        actual.text = unicode(actual_value)

        expected = etree.Element("del", **{"class": "expected"})
        expected.text = element.text

        element.text = None
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
