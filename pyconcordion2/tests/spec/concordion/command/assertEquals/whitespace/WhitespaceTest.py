from __future__ import unicode_literals
from commands import normalize
from base import ConcordionTestCase
from test_rig import TestRig


white_space_mapper = {
    "[SPACE]": " ",
    "[TAB]": "\t",
    "[LF]": "\n",
    "[CR]": "\r",
}


class WhitespaceTest(ConcordionTestCase):
    def whichSnippetsSucceed(self, snippet1, snippet2, evaluationResult):
        return self.which(self.succeeds(snippet1, evaluationResult), self.succeeds(snippet2, evaluationResult))

    def whichSnippetsFail(self, snippet1, snippet2, evaluationResult):
        return self.which(self.fails(snippet1, evaluationResult), self.fails(snippet2, evaluationResult))

    def which(self, b1, b2):
        if b1 and b2:
            return "both"
        elif b1:
            return "the first of"
        elif b2:
            return "the second of"
        return "neither"

    def fails(self, snippet, evaluationResult):
        return not self.succeeds(snippet, evaluationResult)

    def succeeds(self, snippet, evaluationResult):
        t = TestRig()
        t.stub_result(evaluationResult)
        return t.process_fragment(snippet).has_succeeded()

    def normalize(self, s):
        for key, value in white_space_mapper.items():
            s = s.replace(key, value)
        s = normalize(s)
        return s.replace(" ", "[SPACE]")
