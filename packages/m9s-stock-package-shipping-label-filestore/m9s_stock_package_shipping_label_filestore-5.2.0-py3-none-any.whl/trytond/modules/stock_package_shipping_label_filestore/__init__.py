# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock

__all__ = ['register']


def register():
    Pool.register(
        stock.Package,
        module='stock_package_shipping_label_filestore', type_='model')
