from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import logging


class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'

    def action_launch(self):
        self.write({'schedule_type': 'now'})
        return self.action_put_in_queue()

    def action_put_in_queue(self):
        self.write({'state': 'in_queue'})
        cron = self.env.ref('mass_mailing.ir_cron_mass_mailing_queue')
        schedule_dates = self.mapped('schedule_date') or [fields.Datetime.now()]
        for schedule_date in schedule_dates:
            cron._trigger(schedule_date or fields.Datetime.now())

    def action_send_mail(self):
        for mailing in self:
            if not mailing.body_html or mailing.is_body_empty:
                raise UserError(_('El cuerpo del correo está vacío. Por favor, agrega contenido antes de enviar.'))

            # Obtener los destinatarios
            res_ids = mailing._get_recipients()
            if not res_ids:
                raise UserError(_('No hay destinatarios seleccionados.'))

            # Preparar y enviar los correos
            composer_values = {
                'subject': mailing.subject,
                'body': mailing.body_html,
                'email_from': mailing.email_from,
                'attachment_ids': [(4, attachment.id) for attachment in mailing.attachment_ids],
                'reply_to': mailing.reply_to,
                'mail_server_id': mailing.mail_server_id.id,
                'mass_mailing_id': mailing.id,
            }

            composer = self.env['mail.compose.message'].with_context(
                active_model=mailing.mailing_model_real,
                active_ids=res_ids
            ).create(composer_values)

            composer.send_mail()
            mailing.write({'state': 'done', 'sent_date': fields.Datetime.now()})
