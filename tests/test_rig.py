from __future__ import unicode_literals
from io import StringIO
from commands import Commander
import expression_parser


def text_to_bool(text):
    if text.lower() in ("y", "true", "1"):
        return True
    return False


class TestRig(object):
    result = None

    def __init__(self, fixture=None):
        self.fixture = fixture or self

    def stub_result(self, result):
        expression_parser.execute_within_context = lambda x, y: result

    def process_fragment(self, fragment):
        html = """
        <html xmlns:concordion='http://www.concordion.org/2007/concordion'>
          <body>
            <fragment>{}</fragment>
          </body>
        </html>""".format(fragment)
        commander = Commander(self.fixture, StringIO(html))
        commander.process()
        tree = commander.tree
        failures = tree.xpath("//@class='failure'")
        missing = tree.xpath("//@class='missing'")
        exceptions = tree.xpath("//@class='exceptionMessage'")
        return not (failures or missing or exceptions)
