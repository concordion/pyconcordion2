from __future__ import unicode_literals
import unittest

from pyconcordion2 import expression_parser


class ExpressionParserTest(unittest.TestCase):
    def test_variable_only(self):
        expression_str = "test"
        expression_tree = expression_parser.parse(expression_str)
        self.assertEqual(expression_tree.variable_name, expression_str)

    def test_function_only_with_no_parameters(self):
        expression_str = "get_some_thing()"
        expression_tree = expression_parser.parse(expression_str)
        self.assertEqual("get_some_thing", expression_tree.function_name)
        self.assertItemsEqual([], expression_tree.parameters)

    def test_function_only_with_one_parameter(self):
        expression_str = "get_some_thing(param1)"
        expression_tree = expression_parser.parse(expression_str)
        self.assertEqual("get_some_thing", expression_tree.function_name)
        self.assertItemsEqual(["param1"], expression_tree.parameters)

    def test_function_only_with_two_parameters(self):
        expression_str = "get_some_thing(param1, param2)"
        expression_tree = expression_parser.parse(expression_str)
        self.assertEqual("get_some_thing", expression_tree.function_name)
        self.assertItemsEqual(["param1", "param2"], expression_tree.parameters)

    def test_function_only_with_two_parameters_assign_to_variable(self):
        expression_str = "result = get_some_thing(param1, param2)"
        expression_tree = expression_parser.parse(expression_str)
        self.assertEqual("get_some_thing", expression_tree.function_name)
        self.assertItemsEqual(["param1", "param2"], expression_tree.parameters)
        self.assertEqual("result", expression_tree.variable_name)
