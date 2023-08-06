# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice

__all__ = ['register']


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_report_filestore', type_='model')
