from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from afip import Afip
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'


    #TODO: sin terminar

    def get_cuit_status_afip(self):
        self.ensure_one()
        afip_ws = Afip({'CUIT': self.company_id.vat})
        afip_ws.cert = self.company_id.afip_cert
        afip_data =  afip_ws.RegisterInscriptionProof.getTaxpayerDetails(str(self.partner_id.vat))
        # raise ValidationError(f'vat: {self.partner_id.vat} l10n_ar_vat: {self.partner_id.l10n_ar_vat}') 
        raise ValidationError(f'{afip_data}') 
        tax_ids = [self.partner_id.vat]
        taxpayers_details = afip.RegisterInscriptionProof.getTaxpayersDetails(tax_ids)
        