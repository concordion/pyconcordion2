from __future__ import unicode_literals

from spec.concordion.command.verifyRows.results.MissingRowsTest import MissingRowsTest


class SurplusRowsTest(MissingRowsTest):
    def addPerson(self, firstName, lastName):
        super(SurplusRowsTest, self).addPerson(firstName, lastName, 1973)
