# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountInvoiceReportFilestoreTestCase(ModuleTestCase):
    'Test Account Invoice Report Filestore module'
    module = 'account_invoice_report_filestore'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceReportFilestoreTestCase))
    return suite
