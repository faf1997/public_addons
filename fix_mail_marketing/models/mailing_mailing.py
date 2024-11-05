from odoo import models, fields, api

class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'

    def action_launch(self):
        self.write({'schedule_type': 'now'})
        return self.action_send_mails()

    def action_send_mails(self):
        for mailing in self:
            mailing.write({'state': 'sending'})
            mailing._send_mails()
            mailing.write({'state': 'done'})
        return True

    def _send_mails(self):
        MailMail = self.env['mail.mail']
        for mailing in self:
            mailing.ensure_one()
            mailing_model = self.env[mailing.mailing_model_real]
            records = mailing._get_records()
            email_template = mailing._get_email_template()

            for record in records:
                # Generar el correo electrónico basado en la plantilla y el registro
                values = email_template.generate_email(record.id)
                # Crear y enviar el correo
                mail = MailMail.create(values)
                mail.send()
