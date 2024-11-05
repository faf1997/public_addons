from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import logging


class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'


    def action_launch(self):
        self.write({'schedule_type': 'now'})
        return self.action_send_mail()

    