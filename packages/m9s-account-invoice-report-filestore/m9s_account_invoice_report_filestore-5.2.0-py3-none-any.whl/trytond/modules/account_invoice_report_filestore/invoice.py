# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    report_file_id = fields.Char('Report File ID', readonly=True)

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()

        cls.invoice_report_cache.file_id = 'report_file_id'
