# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class StockPackageShippingLabelFilestoreTestCase(ModuleTestCase):
    'Test Stock Package Shipping Label Filestore module'
    module = 'stock_package_shipping_label_filestore'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockPackageShippingLabelFilestoreTestCase))
    return suite
