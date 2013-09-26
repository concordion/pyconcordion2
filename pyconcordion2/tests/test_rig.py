from __future__ import unicode_literals
from io import StringIO
import re

from lxml import etree
from mock import Mock, patch

from commands import Commander


def text_to_bool(text):
    if text.lower() in ("y", "true", "1"):
        return True
    return False


class TestRig(object):
    def __init__(self, fixture=None):
        self.fixture = fixture or self
        self.patcher = None

    def stub_result(self, result):
        if isinstance(result, Exception):
            self.patcher = patch('expression_parser.execute_within_context', new=Mock(side_effect=result))
        else:
            self.patcher = patch('expression_parser.execute_within_context', new=Mock(return_value=result))
        self.patcher.start()

    def process_html(self, html):
        commander = Commander(self.fixture, StringIO(html))
        commander.process()
        self.result = commander.result
        if self.patcher:
            self.patcher.stop()
        return self.result

    def process_fragment(self, fragment):
        html = """
        <html xmlns:concordion='http://www.concordion.org/2007/concordion'>
          <body>
            <fragment>{}</fragment>
          </body>
        </html>""".format(fragment)
        return self.process_html(html)

    def get_output_fragment_xml(self):
        regex = re.compile("</?fragment.*?>")
        return re.sub(regex, "", etree.tostring(self.result.root_element.xpath("//fragment")[0])).strip()

    def success_or_failure(self):
        is_failure = self.result.num_exception or self.result.num_failure
        return "FAILURE" if is_failure else "SUCCESS"
