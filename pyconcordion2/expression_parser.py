from __future__ import unicode_literals

from pyparsing import Word, alphanums, ZeroOrMore, Suppress, Optional, Group

# define grammar
variable_name = Word(alphanums + "_").setResultsName("variable_name")
property_name = Word(alphanums + "_").setResultsName("property_name")
function_name = Word(alphanums + "_").setResultsName("function_name")
parameter_name = Word(alphanums + "_")
equals = Suppress("=")
colon = Suppress(":")
open_parenthesis = Suppress("(")
closed_parenthesis = Suppress(")")
dot = Suppress(".")
comma = Suppress(",")
function_definition = function_name + open_parenthesis + Group(
    Optional(parameter_name + ZeroOrMore(comma + parameter_name))).setResultsName("parameters") + closed_parenthesis

expression = function_definition | variable_name + dot + property_name | (
    variable_name + Optional((equals | colon) + function_definition))


def parse(expression_str):
    return expression.parseString(expression_str)


def execute_within_context(context, expression_str):
    expression_tree = parse(expression_str)
    if expression_tree.function_name:
        fn_name = getattr(context, expression_tree.function_name)
        parameters = [getattr(context, parameter) for parameter in expression_tree.parameters]
        result = fn_name(*parameters)
        if expression_tree.variable_name:
            setattr(context, expression_tree.variable_name, result)
        return result
    elif expression_tree.variable_name:
        variable = getattr(context, expression_tree.variable_name)
        if expression_tree.property_name:
            _property = getattr(variable, expression_tree.property_name)
            return _property
        return variable
