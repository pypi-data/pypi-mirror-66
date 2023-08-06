# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountDeEuerZoneTestCase(ModuleTestCase):
    'Test Account De Euer Zone module'
    module = 'account_de_euer_zone'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountDeEuerZoneTestCase))
    return suite
