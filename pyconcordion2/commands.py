from __future__ import unicode_literals
import expression_parser


class Command(object):
    def __init__(self, element, expression_str, context):
        self.element = element
        self.expression_str = expression_str.replace("#", "")
        self.context = context
        self.children = []

    def run(self):
        pass


class RunCommand(Command):
    pass


class ExecuteCommand(Command):
    def run(self):
        if self.element.tag.lower() == "table":
            for row in get_table_body_rows(self.element):
                for command, element in zip(self.children, row.xpath("td")):
                    command.element = element
                self._run()
        else:
            self._run()

    def _run(self):
        for command in self.children:
            if isinstance(command, SetCommand):
                command.run()
        expression_parser.execute_within_context(self.context, self.expression_str)
        for command in self.children:
            if not isinstance(command, SetCommand):
                command.run()



class VerifyRowsCommand(Command):
    def run(self):
        variable_name = expression_parser.parse(self.expression_str).variable_name
        results = expression_parser.execute_within_context(self.context, self.expression_str)
        for result, row in zip(results, get_table_body_rows(self.element)):
            setattr(self.context, variable_name, result)
            for command, element in zip(self.children, row.xpath("td")):
                command.element = element
                command.run()


def get_table_body_rows(table):
    tr_s = table.xpath("tr")
    return [tr for tr in tr_s if tr.xpath("td")]


class SetCommand(Command):
    def run(self):
        expression = expression_parser.parse(self.expression_str)
        assert expression.variable_name
        setattr(self.context, self.expression_str, self.element.text)


class AssertEqualsCommand(Command):
    def run(self):
        expression_return = expression_parser.execute_within_context(self.context, self.expression_str)
        result = expression_return == self.element.text
        mark_success(result, self.element)


class AssertTrueCommand(Command):
    def run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        mark_success(result, self.element)


class AssertFalseCommand(Command):
    def run(self):
        result = expression_parser.execute_within_context(self.context, self.expression_str)
        mark_success(not result, self.element)


class EchoCommand(Command):
    pass


def mark_success(is_successful, element):
    if is_successful:
        element.attrib["class"] = "success"
    else:
        element.attrib["class"] = "failure"


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
