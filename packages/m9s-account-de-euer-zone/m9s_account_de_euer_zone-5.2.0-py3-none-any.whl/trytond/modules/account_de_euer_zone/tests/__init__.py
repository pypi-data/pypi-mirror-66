# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.account_de_euer_zone.tests.test_account_de_euer_zone import suite
except ImportError:
    from .test_account_de_euer_zone import suite

__all__ = ['suite']
