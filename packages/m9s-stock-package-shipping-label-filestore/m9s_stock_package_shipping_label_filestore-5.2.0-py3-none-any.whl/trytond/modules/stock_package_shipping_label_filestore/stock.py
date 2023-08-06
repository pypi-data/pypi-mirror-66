# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Package(metaclass=PoolMeta):
    __name__ = 'stock.package'

    # Store binaries in the filesystem
    label_file_id = fields.Char('Label File ID', readonly=True)
    label_file_name = fields.Char('Label File Name')

    @classmethod
    def __setup__(cls):
        super(Package, cls).__setup__()
        cls.shipping_label.file_id = 'label_file_id'
        cls.shipping_label.filename = 'label_file_name'
