from __future__ import unicode_literals
from io import StringIO

from mock import Mock, patch

from commands import Commander


def text_to_bool(text):
    if text.lower() in ("y", "true", "1"):
        return True
    return False


class ResultEvent(object):
    def __init__(self, actual, expected):
        self.actual = actual
        self.expected = expected


class Results(object):
    def __init__(self, successes, failures, exceptions):
        self.successes = successes
        self.failures = failures
        self.exceptions = exceptions

    def last_failed_event(self):
        last_failed = self.failures[-1]
        actual = last_failed.xpath("//*[@class='actual']")[0].text
        expected = last_failed.xpath("//*[@class='expected']")[0].text
        return ResultEvent(actual, expected)

    @property
    def failureCount(self):
        return len(self.failures)

    @property
    def exceptionCount(self):
        return len(self.exceptions)

    @property
    def successCount(self):
        return len(self.successes)

    def has_failed(self):
        return self.failureCount or self.exceptionCount

    def has_succeeded(self):
        return not self.has_failed()


class TestRig(object):
    result = None

    def __init__(self, fixture=None):
        self.fixture = fixture or self
        self.patcher = None

    def stub_result(self, result):
        if isinstance(result, Exception):
            self.patcher = patch('expression_parser.execute_within_context', new=Mock(side_effect=result))
        else:
            self.patcher = patch('expression_parser.execute_within_context', new=Mock(return_value=result))
        self.patcher.start()

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

        successes = tree.xpath("//*[@class='success']")
        failures = tree.xpath("//*[@class='failure']")
        missing = tree.xpath("//*[@class='missing']")
        exceptions = tree.xpath("//*[@class='exceptionMessage']")

        self.result = Results(failures=failures, successes=successes, exceptions=exceptions)

        if self.patcher:
            self.patcher.stop()
        return self.result

    def success_or_failure(self):
        is_failure = self.result.exceptionCount or self.result.failureCount
        return "FAILURE" if is_failure else "SUCCESS"
